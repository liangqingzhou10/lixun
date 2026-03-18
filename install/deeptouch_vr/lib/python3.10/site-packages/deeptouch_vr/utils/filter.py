import math
import numpy as np
from scipy.spatial.transform import Rotation as R
from typing import Optional, Dict, List, Tuple

class OneEuroFilter:
    """一阶欧元滤波器用于平滑连续信号"""
    def __init__(self, freq: float, min_cutoff: float = 0.1, beta: float = 0.01, d_cutoff: float = 1.0):
        self.min_cutoff = min_cutoff
        self.beta = beta
        self.d_cutoff = d_cutoff
        self.freq = freq
        self.filtered_value = 0.0
        self.filtered_derivative = 0.0
        self.last_time = None
        self.last_raw_value = None

    def set_freq(self, freq: float):
        self.freq = freq

    def set_mincutoff(self, mincutoff: float):
        self.min_cutoff = mincutoff

    def set_beta(self, beta: float):
        self.beta = beta

    def set_dcutoff(self, dcutoff: float):
        self.d_cutoff = dcutoff

    def apply(self, value: float, timestamp: float) -> float:
        if self.last_time is None:
            self.last_time = timestamp
            self.last_raw_value = value
            self.filtered_value = value
            return value

        dt = timestamp - self.last_time
        if dt <= 0:
            return self.filtered_value

        # 估算导数并调整截止频率
        dx = (value - self.last_raw_value) / dt
        cutoff = self.min_cutoff + self.beta * abs(dx)

        # 低通滤波
        tau = 1.0 / (2.0 * math.pi * cutoff)
        alpha = dt / (tau + dt)
        self.filtered_value = alpha * value + (1 - alpha) * self.filtered_value

        # 对导数做高通滤波
        tau_d = 1.0 / (2.0 * math.pi * self.d_cutoff)
        alpha_d = dt / (tau_d + dt)
        self.filtered_derivative = alpha_d * (self.filtered_value - self.last_raw_value) + (1 - alpha_d) * self.filtered_derivative

        self.last_raw_value = value
        self.last_time = timestamp

        return self.filtered_value

class OneEuroFilterVector3D:
    """三维向量一阶欧元滤波器"""
    def __init__(self, freq: float, min_cutoff: float = 0.1, beta: float = 0.01, d_cutoff: float = 1.0):
        self.filters = [
            OneEuroFilter(freq, min_cutoff, beta, d_cutoff),
            OneEuroFilter(freq, min_cutoff, beta, d_cutoff),
            OneEuroFilter(freq, min_cutoff, beta, d_cutoff)
        ]

    def filter(self, vector, timestamp):
        if vector is None or len(vector) != 3:
            return None
        if isinstance(vector, np.ndarray):
            vector = vector.tolist()
        return [
            self.filters[i].apply(vector[i], timestamp) for i in range(3)
        ]

    def set_freq(self, freq):
        for f in self.filters:
            f.set_freq(freq)
    def set_mincutoff(self, mincutoff):
        for f in self.filters:
            f.set_mincutoff(mincutoff)
    def set_beta(self, beta):
        for f in self.filters:
            f.set_beta(beta)
    def set_dcutoff(self, dcutoff):
        for f in self.filters:
            f.set_dcutoff(dcutoff)



# ---------- 四元数几何工具 & 滤波器（替代原 OneEuroFilterQuat） ----------
def _q_norm(q: List[float]) -> List[float]:
    w, x, y, z = q
    n = math.sqrt(w*w + x*x + y*y + z*z) or 1.0
    return [w/n, x/n, y/n, z/n]

def _q_conj(q: List[float]) -> List[float]:
    w, x, y, z = q
    return [w, -x, -y, -z]

def _q_mul(a: List[float], b: List[float]) -> List[float]:
    aw, ax, ay, az = a; bw, bx, by, bz = b
    return [
        aw*bw - ax*bx - ay*by - az*bz,
        aw*bx + ax*bw + ay*bz - az*by,
        aw*by - ax*bz + ay*bw + az*bx,
        aw*bz + ax*by - ay*bx + az*bw,
    ]

def _q_fix_hemi(q: List[float], ref: List[float]) -> List[float]:
    dot = q[0]*ref[0] + q[1]*ref[1] + q[2]*ref[2] + q[3]*ref[3]
    return [-q[0], -q[1], -q[2], -q[3]] if dot < 0.0 else q

def _slerp(q0: List[float], q1: List[float], u: float) -> List[float]:
    q0 = _q_norm(q0); q1 = _q_norm(q1)
    dot = max(-1.0, min(1.0, q0[0]*q1[0] + q0[1]*q1[1] + q0[2]*q1[2] + q0[3]*q1[3]))
    if dot > 0.9995:
        out = [(1-u)*q0[i] + u*q1[i] for i in range(4)]
        return _q_norm(out)
    theta = math.acos(dot)
    s0 = math.sin((1-u)*theta) / math.sin(theta)
    s1 = math.sin(u*theta) / math.sin(theta)
    return [s0*q0[i] + s1*q1[i] for i in range(4)]

def _so3_log(q: List[float]) -> List[float]:
    w, x, y, z = _q_norm(q)
    w = max(-1.0, min(1.0, w))
    ang = 2.0*math.acos(w)
    s = math.sqrt(max(1e-12, 1.0 - w*w))
    if ang < 1e-8:
        return [0.0, 0.0, 0.0]
    k = ang / s
    return [k*x, k*y, k*z]

def _so3_exp(v: List[float]) -> List[float]:
    vx, vy, vz = v
    th = math.sqrt(vx*vx + vy*vy + vz*vz)
    if th < 1e-8:
        return [1.0, 0.0, 0.0, 0.0]
    s = math.sin(th/2.0) / (th + 1e-12)
    return [math.cos(th/2.0), s*vx, s*vy, s*vz]

def _alpha_from_cutoff(cut_hz: float, dt: float) -> float:
    if cut_hz <= 0.0:
        return 1.0
    tau = 1.0 / (2.0*math.pi*cut_hz)
    return dt / (dt + tau)

class SlerpEMAQuat:
    def __init__(self, freq_hz: float = 120.0, cutoff_hz: float = 5.0):
        self.freq = max(1e-3, float(freq_hz))
        self.cutoff = float(cutoff_hz)
        self._qhat: Optional[List[float]] = None
        self._tprev: Optional[float] = None
    def set_freq(self, f: float): self.freq = max(1e-3, float(f))
    def set_params(self, cutoff_hz: Optional[float] = None, **_):
        if cutoff_hz is not None: self.cutoff = float(cutoff_hz)
    def filter(self, q: List[float], t: float) -> Optional[List[float]]:
        q = _q_norm(q)
        if self._qhat is None:
            self._qhat, self._tprev = q, t
            return self._qhat
        dt = max(1e-4, float(t - (self._tprev or t)))
        self._tprev = t
        alpha = _alpha_from_cutoff(self.cutoff, dt)
        qh = _q_fix_hemi(q, self._qhat)
        self._qhat = _slerp(self._qhat, qh, alpha)
        return self._qhat

class SO3LogLPFQuat:
    def __init__(self, freq_hz: float = 120.0, cutoff_hz: float = 5.0):
        self.freq = max(1e-3, float(freq_hz))
        self.cutoff = float(cutoff_hz)
        self._qhat: Optional[List[float]] = None
        self._vf = [0.0, 0.0, 0.0]
        self._tprev: Optional[float] = None
    def set_freq(self, f: float): self.freq = max(1e-3, float(f))
    def set_params(self, cutoff_hz: Optional[float] = None, **_):
        if cutoff_hz is not None: self.cutoff = float(cutoff_hz)
    def filter(self, q: List[float], t: float) -> Optional[List[float]]:
        q = _q_norm(q)
        if self._qhat is None:
            self._qhat, self._tprev, self._vf = q, t, [0.0, 0.0, 0.0]
            return self._qhat
        dt = max(1e-4, float(t - (self._tprev or t)))
        self._tprev = t
        qh = _q_fix_hemi(q, self._qhat)
        dq = _q_mul(_q_conj(self._qhat), qh)
        v = _so3_log(dq)
        alpha = _alpha_from_cutoff(self.cutoff, dt)
        self._vf = [(1-alpha)*self._vf[i] + alpha*v[i] for i in range(3)]
        self._qhat = _q_norm(_q_mul(self._qhat, _so3_exp(self._vf)))
        return self._qhat
