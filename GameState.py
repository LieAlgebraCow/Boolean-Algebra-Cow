from math import pi
from numpy import sign

from CowBotVector import Vec3
from Conversions import *
from Miscellaneous import rotate_to_range

class GameState:

    def __init__( self,
                  packet = None,
                  utils_game = None,
                  field_info = None,
                  match_settings = None,
                  hitboxes = None,
                  my_index = None,
                  my_team = None,
                  ball_prediction = None,
                  teammate_indices = None,
                  opponent_indices = None,
                  my_old_inputs = None,
                  rigid_body_tick = None,
                  persistent = None):

        self.my_name = packet.game_cars[my_index].name
        self.is_kickoff_pause = packet.game_info.is_kickoff_pause

        #Team info
        self.my_team = my_team
        if self.my_team == 0:
            self.team_sign = 1
        else:
            self.team_sign = -1

        if my_old_inputs.jump == 1:
            me_jumped_last_frame = True
        else:
            me_jumped_last_frame = False

        #The inputs this bot returned last frame.
        self.inputs = my_old_inputs

        self.persistent = persistent

        #Ball info
        self.ball = Ball(packet, self.team_sign)
        self.ball_prediction = ball_prediction

        #My car info
        self.me = CarState(packet = packet,
                           hitboxes = hitboxes,
                           jumped_last_frame = me_jumped_last_frame,
                           index = my_index,
                           team_sign = self.team_sign)
        self.my_index = my_index

        #Other car info
        self.teammates = []
        self.opponents = []

        for i in range(packet.num_cars):
            if i != my_index:
                if i in teammate_indices:
                    self.teammates.append(CarState(packet = packet,
                                                   hitboxes = hitboxes,
                                                   index = i,
                                                   team_sign = self.team_sign))
                else:
                    self.opponents.append(CarState(packet = packet,
                                                   hitboxes = hitboxes,
                                                   index = i,
                                                   team_sign = self.team_sign))
        self.team_mode = None
        if len(self.teammates) == 0:
            self.team_mode = "1v1"
        elif len(self.teammates) == 1:
            self.team_mode = "2v2"
        elif len(self.teammates) == 2:
            self.team_mode = "3v3"
        else:
            self.team_mode = "Other"

        ##################################################################

        #Team kickoff positions
        diagonal_left_spawn = Vec3(2048, -2560, 0)
        diagonal_right_spawn = Vec3(-2048, -2560, 0)
        offcenter_left_spawn = Vec3(256, -3840, 0)
        offcenter_right_spawn = Vec3(-256, -3840, 0)
        far_back_spawn = Vec3(0, -4608, 0)
 
        self.me_diagonal_left = False
        self.me_diagonal_right = False
        self.me_offcenter_left = False
        self.me_offcenter_right = False
        self.me_far_back = False

        if (self.me.pos - diagonal_left_spawn).magnitude() < 50:
            self.me_diagonal_left = True
        elif (self.me.pos - diagonal_right_spawn).magnitude() < 50:
            self.me_diagonal_right = True
        elif (self.me.pos - offcenter_left_spawn).magnitude() < 50:
            self.me_offcenter_left = True
        elif (self.me.pos - offcenter_right_spawn).magnitude() < 50:
            self.me_offcenter_right = True
        elif (self.me.pos - far_back_spawn).magnitude() < 50:
            self.me_far_back = True
 
        self.teammate_diagonal_left = False
        self.teammate_diagonal_right = False
        self.teammate_offcenter_left = False
        self.teammate_offcenter_right = False
        self.teammate_far_back = False
        
        for mate in self.teammates:
            if (mate.pos - diagonal_left_spawn).magnitude() < 50:
                self.teammate_diagonal_left = True
            elif (mate.pos - diagonal_right_spawn).magnitude() < 50:
                self.teammate_diagonal_right = True
            elif (mate.pos - offcenter_left_spawn).magnitude() < 50:
                self.teammate_offcenter_left = True
            elif (mate.pos - offcenter_right_spawn).magnitude() < 50:
                self.teammate_offcenter_right = True
            elif (mate.pos - far_back_spawn).magnitude() < 50:
                self.teammate_far_back = True

        ##################################################################

        self.ball_x_sign = sign(self.ball.pos.x)
        self.teammate_far_post = False
        self.teammate_in_net = False

        far_post_pos = Vec3(-1050*self.ball_x_sign,-5120+140,0)
        in_net_pos = Vec3(0, -5120-60, 0)

        for mate in self.teammates:
            if (mate.pos - far_post_pos).magnitude() < 400:
                self.teammate_far_post = True
            elif (mate.pos - in_net_pos).magnitude() < 400:
                self.teammate_in_net = True

        ##################################################################

        if len(self.teammates) == 2:
            self.number_of_team_in_front_of_ball = 0
            self.ball_behind_me = False
            self.ball_behind_teammate_zero = False
            self.ball_behind_teammate_one = False
            if self.ball.pos.y < self.me.pos.y:
                self.ball_behind_me = True
                self.number_of_team_in_front_of_ball += 1
            if self.ball.pos.y < self.teammates[0].pos.y:
                self.ball_behind_teammate_zero = True
                self.number_of_team_in_front_of_ball += 1
            if self.ball.pos.y < self.teammates[1].pos.y:
                self.ball_behind_teammate_one = True
                self.number_of_team_in_front_of_ball += 1

            self.teammate_zero_ball_side = (self.me.pos.x * self.ball_x_sign < self.teammates[0].pos.x * self.ball_x_sign)
            self.teammate_one_ball_side = (self.me.pos.x * self.ball_x_sign < self.teammates[1].pos.x * self.ball_x_sign)

        ##################################################################

        #Boost info
        self.big_boosts = []
        self.boosts = []
        for index in range(field_info.num_boosts):
            #This way we can pretend we're always on blue.
            if self.team_sign == 1:
                i = index
            else:
                i = 33 - index
            pad = field_info.boost_pads[i]
            pad_pos = Vec3(self.team_sign*pad.location.x,
                           self.team_sign*pad.location.y,
                           pad.location.z)
            self.boosts.append(Boostpad(i,
                                        pad_pos,
                                        packet.game_boosts[i].is_active,
                                        packet.game_boosts[i].timer))
            if pad.is_full_boost:
                self.big_boosts.append(Boostpad(i,
                                                pad_pos,
                                                packet.game_boosts[i].is_active,
                                                packet.game_boosts[i].timer))
        #Mirror the boost list left/right
        self.mirror_boost_list = [0, 2, 1, 4, 3, 6, 5, 7, 9, 8, 11, 10, 14, 13, 12, 18, 17, 16,
                                  15, 21, 20, 19, 23, 22, 25, 24, 26, 28, 27, 30, 29, 32, 31, 33]

        ##################################################################

        #Other Game info
        self.game_time = packet.game_info.seconds_elapsed
        if utils_game != None:
            self.utils_game = utils_game
            self.dt = utils_game.time_delta
            self.utils_game.read_game_information(packet,
                                                  rigid_body_tick,
                                                  field_info)
        else:
            self.dt = 1/120
            self.utils_game = None

        #Minimum distance from the ball to an opponent
        self.opponent_distance = 10000
        for car in self.opponents:
            if (car.pos - self.ball.pos).magnitude() < self.opponent_distance:
                self.opponent_distance = (car.pos - self.ball.pos).magnitude()
            


##################################################################################
#Orientation
##################################################################################

class Orientation:

    '''
    This is an orientation matrix with columns Front, Left, Up.
    This will be the working object for a car or ball orientation.
    '''


    def __init__( self ,
                  pitch = None,
                  yaw = None,
                  roll = None,
                  pyr = None,
                  front = None,
                  left = None,
                  up = None
    ):

        if pitch != None and yaw != None and roll != None:
            pyr = [ pitch, yaw, roll ]

        if pyr != None:
            self.matrix = pyr_to_matrix(pyr)

        if front != None and left != None and up != None:
            self.matrix = [ front, left, up ]

        self.front = self.matrix[0]
        self.left = self.matrix[1]
        self.up = self.matrix[2]

        if pyr != None:
            self.pitch = pyr[0]
            self.yaw = pyr[1]
            self.roll = pyr[2]
        else:
            self.yaw = atan2( self.front.y , self.front.x )
            self.pitch = atan2( self.front.z , sqrt(self.left.z**2 + self.up.z**2) )
            self.roll = atan2( self.left.z , self.up.z )


##################################################################################
#Ball
##################################################################################



def Ball(packet, team_sign, state = None):

    #Packet is used for the current ball state in game.
    #State can be used instead to get a BallState object for a prediction in the future.

    if state == None:

        #Position
        x = packet.game_ball.physics.location.x
        y = packet.game_ball.physics.location.y
        z = packet.game_ball.physics.location.z
        pos = Vec3( team_sign*x, team_sign*y, z )

        #Rotation
        pitch = packet.game_ball.physics.rotation.pitch
        yaw = packet.game_ball.physics.rotation.yaw
        roll = packet.game_ball.physics.rotation.roll            
        rot = Orientation( pitch = pitch,
                           yaw = yaw,
                           roll = roll )
        if team_sign == -1:
            rot = Orientation( pitch = pitch,
                               yaw = rotate_to_range(yaw + pi, [-pi, pi]),
                               roll = roll )

        
        #Velocity
        vx = packet.game_ball.physics.velocity.x
        vy = packet.game_ball.physics.velocity.y
        vz = packet.game_ball.physics.velocity.z
        vel = Vec3( team_sign*vx, team_sign*vy, vz )

        #Angular velocity
        omegax = packet.game_ball.physics.angular_velocity.x
        omegay = packet.game_ball.physics.angular_velocity.y
        omegaz = packet.game_ball.physics.angular_velocity.z
        omega = Vec3( team_sign*omegax, team_sign*omegay, omegaz )

        #Miscellaneous
        latest_touch = packet.game_ball.latest_touch
        hit_location = Vec3(team_sign*latest_touch.hit_location.x,
                            team_sign*latest_touch.hit_location.y,
                            latest_touch.hit_location.z)

    else:
        #Position
        x = state.x
        y = state.y
        z = state.z
        pos = Vec3(team_sign*x, team_sign*y, z)

        #Velocity
        velx = state.velx
        vely = state.vely
        velz = state.velz
        vel = Vec3(team_sign*vx, team_sign*vy, vz)

        #Rotation
        pitch = state.pitch
        yaw = state.yaw
        roll = state.roll
        rot = Orientation( pitch = pitch,
                           yaw = yaw,
                           roll = roll )
        if team_sign == -1:
            rot = Orientation( pitch = pitch,
                               yaw = rotate_to_range(yaw + pi, [-pi,pi]),
                               roll = roll )

        #Angular velocity
        omegax = state.omegax
        omegay = state.omegay
        omegaz = state.omegaz
        omega = Vec3(team_sign*omegax, team_sign*omegay, omegaz)


    return BallState(pos = pos,
                     rot = rot,
                     vel = vel,
                     omega = omega,
                     latest_touch = latest_touch,
                     hit_location = hit_location)


class BallState:

    def __init__( self,
                  pos = None,
                  rot = None,
                  vel = None,
                  omega = None,
                  latest_touch = None,
                  hit_location = None):

        self.pos = None
        self.rot = None
        self.vel = None
        self.omega = None
        
        if pos != None:
            self.x = pos.x
            self.y = pos.y
            self.z = pos.z
            self.pos = pos

        if rot != None:
            self.rot = rot

        if vel != None:
            self.vx = vel.x
            self.vy = vel.y
            self.vz = vel.z
            self.vel = vel

        if omega != None:
            self.omegax = omega.x
            self.omegay = omega.y
            self.omegaz = omega.z
            self.omega = omega

        self.latest_touch = latest_touch
        self.hit_location = hit_location


    #Return a copy of the BallState object, but with given values changed.
    #This will be useful for setting target states.
    def copy_state( self,
                    pos = None,
                    rot = None,
                    vel = None,
                    omega = None):

        if pos != None:
            new_pos = pos
        else:
            new_pos = self.pos

        if vel != None:
            new_vel = vel
        else:
            new_vel = self.vel

        if omega != None:
            new_omega = omega
        else:
            new_omega = self.omega

        if rot != None:
            new_rot = rot
        else:
            new_rot = self.rot

        return BallState(pos = new_pos,
                         rot = new_rot,
                         vel = new_vel,
                         omega = new_omega)




##################################################################################
#Car
##################################################################################

class CarState:

    def __init__(self,
                 packet = None,
                 hitboxes = None,
                 index = None,
                 team_sign = None,
                 label = None,
                 pos = None,
                 rot = None,
                 vel = None,
                 omega = None,
                 demo = None,
                 wheel_contact = None,
                 supersonic = None,
                 jumped = None,
                 double_jumped = None,
                 boost = None,
                 jumped_last_frame = None,
                 hitbox_class = None):

        '''
        Gets the game info for a given car, and returns the values.  Should be fed into a CarState object.
        Never call directly: Only in GameState.__init__() or via CarState.copy_state()
        '''

        if packet != None:
            this_car = packet.game_cars[index]
            self.pos = Vec3( team_sign*this_car.physics.location.x,
                        team_sign*this_car.physics.location.y,
                        this_car.physics.location.z )
            
            yaw = this_car.physics.rotation.yaw
            if team_sign == -1:
                yaw = rotate_to_range(this_car.physics.rotation.yaw + pi, [-pi, pi])
            pitch = this_car.physics.rotation.pitch
            roll = this_car.physics.rotation.roll
            self.rot = Orientation( pitch = pitch,
                                    yaw = yaw,
                                    roll = roll )
            self.vel = Vec3( team_sign*this_car.physics.velocity.x,
                        team_sign*this_car.physics.velocity.y,
                        this_car.physics.velocity.z )
            self.omega = Vec3( team_sign*this_car.physics.angular_velocity.x,
                          team_sign*this_car.physics.angular_velocity.y,
                          this_car.physics.angular_velocity.z )
            self.demo = this_car.is_demolished
            self.wheel_contact = this_car.has_wheel_contact
            self.supersonic = this_car.is_super_sonic
            self.jumped = this_car.jumped
            self.double_jumped = this_car.double_jumped
            self.boost = this_car.boost
            self.hitbox_class = Hitbox(this_car)
     
            self.jumped_last_frame = jumped_last_frame
            self.index = index
            self.label = label

        else:
            self.pos = pos
            self.rot = rot
            self.vel = vel
            self.omega = omega
        
            self.demo = demo
            self.wheel_contact = wheel_contact
            self.supersonic = supersonic
            self.jumped = jumped
            self.double_jumped = double_jumped
            self.boost = boost
            self.index = index
            self.hitbox_class = hitbox_class
        
            self.jumped_last_frame = jumped_last_frame


    #Return a copy of the CarState object, but with given values changed.
    #This will be useful for setting target states.
    def copy_state(self,
                   pos = None,
                   vel = None,
                   omega = None,
                   rot = None,
                   boost = None):
        
        if pos != None:
            new_pos = pos
        else:
            new_pos = self.pos

        if vel != None:
            new_vel = vel
        else:
            new_vel = self.vel

        if omega != None:
            new_omega = omega
        else:
            new_omega = self.omega

        if rot != None:
            new_rot = rot
        else:
            new_rot = self.rot

        if boost != None:
            new_boost = boost
        else:
            new_boost = self.boost
            

        return CarState(pos = new_pos,
                        rot = new_rot,
                        vel = new_vel,
                        omega = new_omega,
                        demo = self.demo,
                        wheel_contact = self.wheel_contact,
                        supersonic = self.supersonic,
                        jumped = self.jumped,
                        double_jumped = self.double_jumped,
                        boost = new_boost,
                        jumped_last_frame = self.jumped_last_frame,
                        index = self.index)


##################################################################################

##################################################################################

class Boostpad:

    def __init__(self, index, pos, is_active, timer):
        self.index = index
        self.pos = pos
        self.is_active = is_active
        self.timer = timer


##################################################################################

##################################################################################

class Hitbox:

    def __init__( self,
                  car = None ):


        self.widths = [ car.hitbox.length, car.hitbox.width, car.hitbox.height ]
        self.offset = [ car.hitbox_offset.x, car.hitbox_offset.y, car.hitbox_offset.z ]
        self.half_widths = [ width / 2 for width in self.widths ]








