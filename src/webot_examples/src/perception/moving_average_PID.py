class MovingAverage:

    def __init__(self, n):
        self.samples = n
        self.data = []
        self.weights = list(range(1, n + 1))

    def add_sample(self, new_sample):
        if len(self.data) < self.samples:
            self.data.append(new_sample)
        else:
            self.data = self.data[1:] + [new_sample]
            
    def get_sample_count(self):
        return len(self.data)
        
    def get_mm(self):
        return float(sum(self.data)) / len(self.data)

    def get_wmm(self):
        s = 0
        for i, x in enumerate(self.data):
            s += x * self.weights[i]
        return float(s) / sum(self.weights[:len(self.data)])


class PID():

    def __init__(self,kp,ki,kd):

        self.Kp=kp
        self.Ki=ki
        self.Kd=kd
        self.p_error=0.0
        self.i_error=0.0
        self.d_error=0.0

    def pid_control(self,cte):

        self.d_error=cte-self.p_error
        self.p_error=cte
        self.i_error+=cte

        return self.Kp*self.p_error + self.Ki*self.i_error + self.Kd*self.d_error