from mass_object import Mass
import math

class World:
    def __init__(self, masses=[], time_step=1):
        self.masses = masses
        self.time_step = time_step

    def create_mass(self, mass, pos=[0, 0], vel_vec=[0, 0], immovable=False):
        new_mass = Mass(mass, pos, vel_vec, immovable)
        self.masses.append(new_mass)

        return new_mass

    def get_r_vec(self, mass1, mass2):
        delta_x = mass2.pos[0] - mass1.pos[0]
        delta_y = mass2.pos[1] - mass1.pos[1]
        return [delta_x, delta_y]

    def get_r(self,r_vec):
        r = math.sqrt(r_vec[1]**2 + r_vec[0]**2)
        return r
    
    def get_acc_vec(self, mass2, r_vec):
        G = 6.6743 * (10**-11)
        r = self.get_r(r_vec)

        acc_x = G*(mass2.mass/r**3)*r_vec[0]
        acc_y = G*(mass2.mass/r**3)*r_vec[1]
        return [acc_x, acc_y]
    
    def new_vel_vec(self, mass1, mass2):
        if mass1 == mass2:
            return mass1.vel_vec
        
        r_vec = self.get_r_vec(mass1, mass2)
        acc_vec = self.get_acc_vec(mass2, r_vec)
        vel_vec = [0, 0]
        for i in range(2):
            vel_vec[i] = mass1.vel_vec[i] + acc_vec[i]*self.time_step
        
        return vel_vec
    
    def update_vel_vec(self, mass1, mass2):
        new_vel_vec = self.new_vel_vec(mass1, mass2)
        mass1.vel_vec = new_vel_vec
    
    def update_pos_vec(self, mass):
        for i in range(2):
            mass.pos[i] += mass.vel_vec[i]
    
    def update_world(self, n_time_steps=1):
        for k in range(n_time_steps):
            for i in range(len(self.masses)):
                if self.masses[i].immovable == False:
                    for j in range(len(self.masses)):
                        if i != j:
                            self.update_vel_vec(self.masses[i], self.masses[j])
            for i in range(len(self.masses)):
                if self.masses[i].immovable == False:
                    self.update_pos_vec(self.masses[i])
    
    def __str__(self):
        string = ""
        for i in range(len(self.masses)):
            string += f"Mass number {i}.\nMass: {self.masses[i].mass}\nVelocity vector: {self.masses[i].vel_vec}\nPosition vector: {self.masses[i].pos}"
            string += "\n"
        return string