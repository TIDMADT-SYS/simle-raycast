import pygame,sys
from math import *
from pygame.locals import *

music_file = '01.-Stones-Chamber.mp3'
pygame.init()
pygame.mixer.init()
pygame.mixer.music.load(music_file)
pygame.mixer.music.play()

BLACK=pygame.color.THECOLORS["black"]
WHITE=pygame.color.THECOLORS["white"]
BLUE=(  0,   0, 255)
GREY=(245, 245, 245)
CLOCK=pygame.time.Clock()
#Open Pygame window
WIDTH,HEIGHT=640,480
screen = pygame.display.set_mode((WIDTH, HEIGHT),) #add RESIZABLE ou FULLSCREEN
#title
pygame.display.set_caption("raycaster - FPS Mode")

grid=[[1,1,1,1,1,1,1,1,1,1],
      [1,0,0,0,0,0,0,0,0,1],
      [1,0,0,0,0,2,2,2,0,1],
      [1,0,0,0,0,0,0,2,0,1],
      [1,0,2,2,2,0,0,2,0,1],
      [1,0,2,0,0,0,0,0,0,1],
      [1,0,2,0,0,0,0,0,0,1],
      [1,0,0,0,0,0,0,0,0,1],
      [1,1,1,1,1,1,1,1,1,1]]
wall_type = 0;

texture_floor=pygame.image.load('walls/colorstone.png').convert()
texture_ceiling=pygame.image.load('walls/wood.png').convert()

#normal dungeon tiles
multi_texture = [
    pygame.image.load('walls/mossy.png').convert(),
    pygame.image.load('walls/greystone.png').convert(),
]

ground=pygame.Surface((640,240)).convert();ground.fill((0,100,0))
x_limit=len(grid[0]);y_limit=len(grid)
#put resolution value to 1 for a clear display but it will be too slow
resolution=3
wall_hit=0
#field of view (FOV) 
fov=60
grid_height=64;grid_width=64;wall_height=64;wall_width=64
player_height=wall_height/2
player_pos=[160,224]
view_angle=0

#Dimension of the Projection Plane
projection_plane=[WIDTH, HEIGHT]
#Center of the Projection Plane
plane_center=HEIGHT//2 #[WIDTH/2, HEIGHT/2]
#distance from player to projection plane
to_plane_dist=int((WIDTH/2)/tan(radians(fov/2)))
#Angle between subsequent rays
angle_increment=fov/WIDTH
#angle of the casted ray
ray_angle=view_angle+(fov/2)

# my additions, to seperate the animation from the keypress, causing a trigger
left_rotation_trigger = 0
right_rotation_trigger = 0
move_trigger = 0
debug_pos = 1

move_speed=16
x_move=int(move_speed*cos(radians(view_angle)))
y_move=-int(move_speed*sin(radians(view_angle)))
rotation_speed=10

pygame.key.set_repeat(400, 30)

while True:
    
    #loop speed limitation
    #30 frames per second is enough
    CLOCK.tick(30)
    
    for event in pygame.event.get():    #wait for events
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
            
    #Movement controls
    keys = pygame.key.get_pressed()
 
    if move_trigger>0:
       player_pos[0]+=x_move
       player_pos[1]+=y_move
       move_trigger -= move_speed
    elif right_rotation_trigger>0:
         #this is where we actually do the right rotation
       view_angle-=rotation_speed
       if view_angle<0:view_angle+=360
       x_move=int(move_speed*cos(radians(view_angle)))
       y_move=-int(move_speed*sin(radians(view_angle)))
       right_rotation_trigger -= rotation_speed
    elif left_rotation_trigger>0:
       view_angle+=rotation_speed
       if view_angle>359:view_angle-=360
       x_move=int(move_speed*cos(radians(view_angle)))
       y_move=-int(move_speed*sin(radians(view_angle)))               
       left_rotation_trigger -= rotation_speed
    else:
        #we are done moving and rotating, we can see is there is another move
        if debug_pos>0:
            #print("x pos = " , player_pos[0]/64)
            #print("y pos = " , player_pos[1]/64)
            debug_pos=0
        if keys[K_UP]:
            #need to check and see if you CAN move
            dest_x = (player_pos[0] + (x_move*4))/64
            dest_y = (player_pos[1] + (y_move*4))/64

            #print("attempting to move to " , dest_x , " " , dest_y)
            if grid[int(dest_y)][int(dest_x)]>0:
                wall_type = grid[int(dest_y)][int(dest_x)]
                print("there is a wall there - type ", wall_type)
            else:
                #print("you can move")
                move_trigger += 64
                debug_pos = 1
        elif keys[K_LEFT]:
            left_rotation_trigger += 90
        elif keys[K_RIGHT]:
            right_rotation_trigger += 90
   
    #angle of the first casted ray
    ray_angle=view_angle+(fov/2)
    
    for x in range(0,WIDTH,resolution):
          
        if ray_angle<0:ray_angle+=360
        if ray_angle>359:ray_angle-=360
        if ray_angle==0:ray_angle+=0.01

        #tx and ty used to correct tangent direction
        if ray_angle>=0 and ray_angle<=90:tx=1;ty=-1#tan is(+)
        elif ray_angle>=91 and ray_angle<=180:tx=1;ty=1#tan is(-)
        elif ray_angle>=181 and ray_angle<=270:tx=-1;ty=1#tan is(+)
        elif ray_angle>=271 and ray_angle<=360:tx=-1;ty=-1#tan is(-)
        
        wall_hit=0;hor_wall_dist=ver_wall_dist=100000
        #(y_side)whether ray hit part of the block above the line,or the block below the line
        if ray_angle>=0 and ray_angle<=180:
           y_side=-1;signed_y=-1
        else:y_side=grid_height;signed_y=1
        #(x_side)whether ray hit left part of the block of the line,or the block right of the line
        if ray_angle>=90 and ray_angle<=270:
           x_side=-1;signed_x=-1
        else:x_side=grid_width;signed_x=1

        #tangante of the casted ray angle
        tan_angle=tan(radians(ray_angle))
        #first horizontal y step
        y_step=(player_pos[1]//grid_height)*(grid_height)+y_side
        #first horizontal x step (+0.4 to correct wall position)
        x_step=(player_pos[0]+abs(player_pos[1]-y_step)/tan_angle*tx)+0.4
        ray_x=x_step;ray_y=y_step
        ray_pos=[int(ray_y//grid_height),int(ray_x//grid_width)]
        #if there is a wall there
        if ray_pos[0]>=0 and ray_pos[0]<y_limit and  ray_pos[1]>=0 and ray_pos[1]<x_limit:
         if grid[ray_pos[0]][ray_pos[1]]>0:
           wall_type = grid[ray_pos[0]][ray_pos[1]]
           #finding distance to horizontal wall
           hor_wall_dist=int(sqrt((player_pos[0]-ray_x)**2+(player_pos[1]-ray_y)**2));wall_hit=1
         else:
           #from now horizontal x_step and y_step will remind the same for the rest of the casted ray
           x_step=(grid_height/tan_angle*tx);y_step=grid_height*signed_y
           ray_x+=x_step;ray_y+=y_step
           ray_pos=[int(ray_y//grid_height),int(ray_x//grid_width)]
           if ray_pos[0]>=0 and ray_pos[0]<y_limit and  ray_pos[1]>=0 and ray_pos[1]<x_limit:
            if grid[ray_pos[0]][ray_pos[1]]>0:
              wall_type = grid[ray_pos[0]][ray_pos[1]]
              #finding distance to horizontal wall
              hor_wall_dist=int(sqrt((player_pos[0]-ray_x)**2+(player_pos[1]-ray_y)**2));wall_hit=1
            else:
             while True:
                #remember that horizontal x_step and y_step will remind the same for the rest of the casted ray
                ray_x+=x_step;ray_y+=y_step
                ray_pos=[int(ray_y//grid_height),int(ray_x//grid_width)]
                if ray_pos[0]>=0 and ray_pos[0]<y_limit and  ray_pos[1]>=0 and ray_pos[1]<x_limit:
                 if grid[ray_pos[0]][ray_pos[1]]>0:
                   wall_type = grid[ray_pos[0]][ray_pos[1]]
                   #finding distance to horizontal wall
                   hor_wall_dist=int(sqrt((player_pos[0]-ray_x)**2+(player_pos[1]-ray_y)**2));wall_hit=1
                   break
                else:break
        hor_wall_pos=ray_x
        
        #first vertical x step
        x_step=(player_pos[0]//grid_width)*(grid_width)+x_side
        #first vertical y step
        y_step=(player_pos[1]+abs(player_pos[0]-x_step)*tan_angle*ty)
        ray_x=x_step;ray_y=y_step
        ray_pos=[int(ray_y//grid_height),int(ray_x//grid_width)]
        #if there is a wall there
        if ray_pos[0]>=0 and ray_pos[0]<y_limit and  ray_pos[1]>=0 and ray_pos[1]<x_limit:
         if grid[ray_pos[0]][ray_pos[1]]>0:
           wall_type = grid[ray_pos[0]][ray_pos[1]]
           #finding distance to vertical wall
           ver_wall_dist=int(sqrt((player_pos[0]-ray_x)**2+(player_pos[1]-ray_y)**2));wall_hit=1
         else:
          #from now verticaal x_step and y_step will remind the same for the rest of the casted ray
          x_step=grid_width*signed_x;y_step=(grid_width*tan_angle*ty)
          ray_x+=x_step;ray_y+=y_step
          ray_pos=[int(ray_y//grid_height),int(ray_x//grid_width)]
          if ray_pos[0]>=0 and ray_pos[0]<y_limit and  ray_pos[1]>=0 and ray_pos[1]<x_limit:
           if grid[ray_pos[0]][ray_pos[1]]>0:
             wall_type = grid[ray_pos[0]][ray_pos[1]]
             #finding distance to vertical wall
             ver_wall_dist=int(sqrt((player_pos[0]-ray_x)**2+(player_pos[1]-ray_y)**2));wall_hit=1
           else:
             while True:
                #remember that vertical x_step and y_step will remind the same for the rest of the casted ray
                ray_x+=x_step;ray_y+=y_step
                ray_pos=[int(ray_y//grid_height),int(ray_x//grid_width)]
                if ray_pos[0]>=0 and ray_pos[0]<y_limit and  ray_pos[1]>=0 and ray_pos[1]<x_limit:
                 if grid[ray_pos[0]][ray_pos[1]]>0:
                   wall_type = grid[ray_pos[0]][ray_pos[1]]
                   #finding distance to horizontal wall
                   ver_wall_dist=int(sqrt((player_pos[0]-ray_x)**2+(player_pos[1]-ray_y)**2));wall_hit=1
                   break
                else:break
        ver_wall_pos=ray_y
        
        if wall_hit:         
           #chosing the closer distance          
           wall_dist=min(hor_wall_dist,ver_wall_dist)
           if wall_dist==hor_wall_dist:wall_side=1
           elif wall_dist==ver_wall_dist:wall_side=2

           #to find the texture position with pressision
           if wall_side==1:wall_pos=int(hor_wall_pos)
           elif wall_side==2:wall_pos=int(ver_wall_pos)
           #finding the texture position
           texture_pos=int(wall_pos%wall_width)
           #invert the texture position for correction(-0.1 is to avoid error)
           if wall_side==1 and y_side==grid_height \
           or wall_side==2 and x_side==-1:
              texture_pos=int((wall_width-0.1)-texture_pos)
           #beta is the angle of the ray that is being cast relative to the viewing angle
           beta=radians(view_angle-ray_angle)
           cos_beta=cos(beta)
           #removing fish-eye effect
           wall_dist=(wall_dist*cos_beta)
           #Extract the part-column from the texture using the subsurface method:
           column=multi_texture[wall_type-1].subsurface(texture_pos,0,1,wall_height)       
           #finding the height of the projected wall slice
           slice_height=int(wall_height/wall_dist*to_plane_dist)
           #Scale it to the height at which we're going to draw it using transform.scale
           column = pygame.transform.scale(column, (resolution, slice_height))
           #the top position where the wall slice should be drawn
           slice_y=plane_center-(slice_height//2)
           
           #now floor-casting and ceilings
           cos_angle=cos(radians(ray_angle))
           sin_angle=-sin(radians(ray_angle))
           #begining of floor
           wall_bottom=slice_y+slice_height
           #begining of ceilings
           wall_top=slice_y
           #wall_bottom=plane_center+25
           #wall_top=plane_center-25
           while wall_bottom<HEIGHT:
              wall_bottom+=resolution
              wall_top-=resolution
              #(row at floor point-row of center)
              row=wall_bottom-plane_center
              #straight distance from player to the intersection with the floor 
              straight_p_dist=(player_height/row*to_plane_dist)
              #true distance from player to floor
              to_floor_dist=(straight_p_dist/cos_beta)
              #coordinates (x,y) of the floor
              ray_x=int(player_pos[0]+(to_floor_dist*cos_angle))
              ray_y=int(player_pos[1]+(to_floor_dist*sin_angle))
              #the texture position
              floor_x=(ray_x%wall_width);floor_y=(ray_y%wall_height)

              # this draws the floor
              screen.blit(texture_floor,(x,wall_bottom),(floor_x,floor_y,resolution,resolution))

              #this puts on a ceiling... only do if inside
              screen.blit(texture_ceiling,(x,wall_top),(floor_x,floor_y,resolution,resolution))
           
           #drawing everything
           screen.blit(column,(x,slice_y))#;screen.blit(shadow,(x,slice_y))
        ray_angle-=angle_increment*resolution
    
    #measure the framerate   
    #print(CLOCK.get_fps())
    pygame.display.flip()
    screen.fill(BLACK)
    screen.blit(ground,(0,240))
