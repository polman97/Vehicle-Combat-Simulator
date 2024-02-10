import random

#TODO annotations :)
#TODO double triple quadruple check math is working.
def pen_calculator(base_pen_chance, armour_stripped, max_armor_stripped, ammo_bonus, dist):
    if ammo_bonus != 2.5:
        range_bonus = max(0, (30-dist))
    else:
        range_bonus = 0
    pen_chance  = min(100,(min(max_armor_stripped,max(base_pen_chance,armour_stripped))*ammo_bonus+range_bonus))
    return pen_chance
class Vehicle():
    def __init__(self, stats, dist, armor_state):
        self.vehicle_stats = stats.copy() ## very important, apparently python just changes the base variable as it takes damage/armor damage
        self.distance = dist
        ## armor needs some math as we have the slider that changes armor state, and the penchance formula wants % of armor missing from total as an imput
        self.vehicle_stats['current armor'] = (self.vehicle_stats['armor']*(armor_state/100))
        self.vehicle_stats['armor stripped'] = 100-((self.vehicle_stats['current armor']/self.vehicle_stats['armor'])*100)

    def shoot(self, target, dist, timer):
        rand = random.randint(0,100)
        penchance = pen_calculator(target.vehicle_stats['base penchance'], target.vehicle_stats['armor stripped'], target.vehicle_stats['max penchance'],self.vehicle_stats['pen multiplier'], dist)
        if rand <= penchance:
            print(f'{self.vehicle_stats['name']} hit {target.vehicle_stats['name']} at {timer}s. penchance: {penchance}, randit: {rand}')
            target.get_hit(self.vehicle_stats['damage'], self.vehicle_stats['damage type'])

            # checks for gun 2, shoots again if so (all vehicles with 2 guns have same reload on both guns
        else:
            print(f'{self.vehicle_stats['name']} missed {target.vehicle_stats['name']} at {timer}s. penchance: {penchance}, randit: {rand}')
        if self.vehicle_stats['damage gun 2'] > 0:
            rand2 = random.randint(0, 100)
            penchance2 = pen_calculator(target.vehicle_stats['base penchance'], target.vehicle_stats['armor stripped'],
                                       target.vehicle_stats['max penchance'], self.vehicle_stats['pen multiplier gun 2'],
                                       dist)
            if rand2 <= penchance2:
                target.get_hit(self.vehicle_stats['damage gun 2'], self.vehicle_stats['damage type gun 2'])
                print(f'{self.vehicle_stats['name']} hit {target.vehicle_stats['name']} at {timer}s. penchance: {penchance}, randit: {rand}')
            else:
                print(f'{self.vehicle_stats['name']} missed {target.vehicle_stats['name']} at {timer}s. penchance: {penchance2}, randit: {rand2}')

    def get_hit(self, damage, damage_type):
        #idk if there's a prettier way of checking for damage type, this is kinda ugleh, but t works
        if damage_type == 'explosive':
            self.vehicle_stats['hp'] = self.vehicle_stats['hp'] - (damage * 0.85)
            self.vehicle_stats['current armor'] = self.vehicle_stats['current armor'] - (damage * 0.85)
        if damage_type == 'ap':
            self.vehicle_stats['hp'] = self.vehicle_stats['hp'] - damage
            self.vehicle_stats['current armor'] = self.vehicle_stats['current armor'] - damage
        if damage_type == 'demolition':
            self.vehicle_stats['hp'] = self.vehicle_stats['hp'] - (damage * 0.3)
            self.vehicle_stats['current armor'] = self.vehicle_stats['current armor'] - (damage * 0.3)
        self.vehicle_stats['armor stripped'] = 100 - (
                    (self.vehicle_stats['current armor'] / self.vehicle_stats['armor']) * 100)
        print(f'{self.vehicle_stats['name']} hp: {self.vehicle_stats['hp']}')
def vehicle_1v1(vehicle1a, vehicle2a, dist, iterations, armor_percentage1, armor_percentage2):
    tankalive = True
    vehicle1_wins = 0
    vehicle2_wins = 0
    timelist = []
    for i in range(iterations):
        timer = 0
        tankalive = True
        vehicle1 = Vehicle(vehicle1a, dist, armor_percentage1)
        vehicle2 = Vehicle(vehicle2a, dist, armor_percentage2)
        print(vehicle1.vehicle_stats)
        print(vehicle2.vehicle_stats)
        while tankalive == True:
            if timer == 0 or timer % vehicle1.vehicle_stats['reload+firing'] == 0:
                vehicle1.shoot(vehicle2, dist, timer)
            if timer == 0 or timer % vehicle2.vehicle_stats['reload+firing'] == 0:
                vehicle2.shoot(vehicle1, dist, timer)
            if vehicle1.vehicle_stats['hp'] <= 0:
                vehicle2_wins += 1
                timelist.append(timer)
                print(f'{vehicle2.vehicle_stats['name']} wins at {timer}s')
                print('-------------------------------------------')
                tankalive = False
            if vehicle2.vehicle_stats['hp'] <= 0:
                vehicle1_wins += 1
                timelist.append(timer)
                print(f'{vehicle2.vehicle_stats['name']} wins at {timer}s')
                tankalive = False
                print('-------------------------------------------')
            timer += 0.25
    avgtime = sum(timelist) / len(timelist)
    print(f'{vehicle1a['name']} wins: {vehicle1_wins}, {vehicle2a['name']} wins: {vehicle2_wins}, average time: {avgtime}s')
    return vehicle1_wins, vehicle2_wins, avgtime




