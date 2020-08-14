    def load_config(self,file_name):
        result = []
        f = open(file_name, "r")
        for line in f.readlines() :
            result.append(line.strip('\n'))

        for i in range(len(result)) :
            if result[i] == '==World==' :
                gravity_re = result[i + 1]
                gravity = re.findall(r'(\d+)', gravity_re)
                a = int(gravity[0])
                self._gravity = range(0,a)
                start_level = result[i + 2]
                level = start_level.split(' ')
                self._level_name = level[2]
            if result[i] == '==Player==' :
                character_re = result[i + 1]
                character = character_re.split(' ')
                b = character[2]
                x_re = result[i + 2]
                x = re.findall(r'(\d+)', x_re)
                x = int(x[0])
                y_re = result[i + 3]
                y = re.findall(r'(\d+)', y_re)
                y = int(y[0])
                mass_re = result[i + 4]
                mass = re.findall(r'(\d+)', mass_re)
                mass = int(mass[0])
                health_re = result[i + 5]
                health = re.findall(r'(\d+)', health_re)
                self._health = int(health[0])
                velocity_re = result[i + 6]
                velocity = re.findall(r'(\d+)', velocity_re)
                velocity = int(velocity[0])
