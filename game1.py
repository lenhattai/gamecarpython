import pygame
from pygame.locals import *
import random
pygame.init()
#màu nền
xam=(100,100,100)
trang=(255,255,255)
hong=(255,192,203)
cam=(255,165,0)
# tạo cửa sổ
rong= 500
dai=500
sizemanhinh=(rong,dai)
manhinh= pygame.display.set_mode(sizemanhinh)
pygame.display.set_caption('Logistic game')
icon=pygame.image.load(r'C:\\Users\\ADMIN\\Downloads\\pythongame\\game1\\picture\UEH.png')
pygame.display.set_icon(icon)
# khởi tạo biến
gameplay=False
tocdo=2
diem=0
#đường xe chạy
rộngđường=300
biên_rộng=10
biên_dài=50
#lane đường
lane_trái=150
lane_giữa=250
lane_phải=350
lanes=[lane_trái,lane_giữa,lane_phải]
lane_y=0
#đường và biên
đường=(100,0,rộngđường,dai)
biên_trái=(95,0,biên_rộng,dai)
biên_phải=(400,0,biên_rộng,dai)
#vị trí ban đầu của xe:
xe_x=250
xe_y=400
#chướng ngại vật
class chuongngaivat(pygame.sprite.Sprite):
    # hàm khởi tạo
    def __init__(self, image, x, y): 
        pygame.sprite.Sprite.__init__(self)
        #canh chỉnh hình
        
        self.image=pygame.transform.scale(image,(50,100))
        self.rect=self.image.get_rect()
        self.rect.center=(x,y)
class xechohang(chuongngaivat):
    # hàm khởi tạo
    def __init__(self,x,y):
        image1=pygame.image.load(r'C:\Users\ADMIN\Downloads\pythongame\game1\picture\xechohang.png')
        super().__init__(image1,x,y)
class boost(pygame.sprite.Sprite):
    # hàm khởi tạo
    def __init__(self,image,x,y):
        pygame.sprite.Sprite.__init__(self)
        #canh chỉnh hình
        
        self.image=pygame.transform.scale(image,(50,100))
        self.rect=self.image.get_rect()
        self.rect.center=(x,y)
        
xe_group= pygame.sprite.Group()
chuongngaivat_group= pygame.sprite.Group()
boost_group=pygame.sprite.Group()
# tạo xe người chơi
Player=xechohang(xe_x,xe_y)
xe_group.add(Player)
#load chuongngaivat
image_name=['car.png','pickup_truck.png','semi_trailer.png','taxi.png','van.png']
chuongngaivat_image=[]
for name in image_name:
    image=pygame.image.load(r'C:\\Users\\ADMIN\\Downloads\\pythongame\\game1\\picture\\' + name)
    chuongngaivat_image.append(image)
# tạo boost
image1_name=['A.png','A+.png']
boost_image=[]
for i in image1_name:
    image1=pygame.image.load(r'C:\\Users\\ADMIN\\Downloads\\pythongame\\game1\\picture\\' + i)
    boost_image.append(image1)


#load hình va chạm:
crash=pygame.image.load(r'C:\\Users\\ADMIN\\Downloads\\pythongame\\game1\\picture\\crash.png')
crash_rect=crash.get_rect()
#Vòng lặp xử lí game
#cài đặt fps(cho mượt game)
clock=pygame.time.Clock()
fps=150
chaygame=True
gameover=False
while chaygame:
    # chỉnh frame hình trên giây
    clock.tick(fps)
    for event in pygame.event.get():
        if event.type==QUIT:
            chaygame=False
        #điều khiển xe:
        if event.type==KEYDOWN :
            if event.key== K_LEFT and Player.rect.center[0]>lane_trái:
                Player.rect.x -=100
            if event.key== K_RIGHT and Player.rect.center[0]<lane_phải:
                Player.rect.x +=100
            if event.key==K_b and diem >2:
                tocdo+=2
                diem-=2
            if event.key==K_c and diem >1:
                tocdo-=1
                diem-=1
            if event.key==K_o:
                tocdo=0 
            if event.key==K_p:
                tocdo=2
        #kiểm tra va chạm
        for xecongcong in chuongngaivat_group:
           if pygame.sprite.collide_rect(Player,xecongcong):
              gameover=True
    #check va chạm khi xe đừng yên
    if pygame.sprite.spritecollide(Player,chuongngaivat_group,True):
        gameover=True
        crash_rect.center=[Player.rect.center[0],Player.rect.top]
        #kiếm tra khi đi qua A+
        for A in boost_group:
            if pygame.sprite.collide_rect(Player,A):
                diem+=1
    if pygame.sprite.spritecollide(Player,boost_group,True):
        diem+=1
    #vẽ địa hình 
    manhinh.fill(hong)
    #vẽ đường 
    pygame.draw.rect(manhinh,xam,đường)
    #vẽ biên 
    pygame.draw.rect(manhinh,cam,biên_trái)
    pygame.draw.rect(manhinh,cam,biên_phải)
    #vẽ lane đường 
    lane_y+=tocdo
    if lane_y >= biên_dài*2:
        lane_y=0
    for y in range(biên_dài*-2,dai,biên_dài*2):
        pygame.draw.rect(manhinh,trang,(lane_trái+45,y+lane_y,biên_rộng,biên_dài))
        pygame.draw.rect(manhinh,trang,(lane_phải-45,y+lane_y,biên_rộng,biên_dài))
    #vẽ xe 
    xe_group.draw(manhinh)
    #vẽ chướng ngại vật
    #1.đặt ngẫu nhiên xe và giảm số lần xuất hiện của xe
    if len(chuongngaivat_group) <2 :
        add_chuongngaivat=True
        for xecongcong in chuongngaivat_group:
            if xecongcong.rect.top < xecongcong.rect.height * 1.5 :
                 add_chuongngaivat=False
        if add_chuongngaivat:
           lane=random.choice(lanes)
           image=random.choice(chuongngaivat_image)
           xecongcong=chuongngaivat(image,lane,dai/ -2)
           chuongngaivat_group.add(xecongcong)
    # đặt A+ ngẫu nhiên
    if len(boost_group) <2 :
        add_boost=True
        for A in boost_group:
            if A.rect.top < A.rect.height * 1.5 :
                 add_boost=False
        if add_boost:
           lane=random.choice(lanes)
           image=random.choice(boost_image)
           A=boost(image,lane,dai/ -2)
           boost_group.add(A)
    #cho xe công cộng chạy
    for xecongcong1 in chuongngaivat_group :
        xecongcong1.rect.y +=tocdo
        # xóa xe ra khỏi màn hình
        if xecongcong1.rect.top >= dai:
           xecongcong1.kill()
           diem +=1 
           if diem > 0 and diem % 10==0:
               tocdo+=1
    chuongngaivat_group.draw(manhinh)
    for boost1 in boost_group :
        boost1.rect.y +=tocdo
        # xóa A+ ra khỏi màn hình
        if boost1.rect.top >= dai:
           boost1.kill()
           
    boost_group.draw(manhinh)
    #hiển thị điểm 
    font=pygame.font.Font(pygame.font.get_default_font(),16)
    text=font.render('Score: ' +str(diem),True,trang)
    text_rect=text.get_rect()
    text_rect.center=(50,250)
    manhinh.blit(text,text_rect)
    font1=pygame.font.Font(pygame.font.get_default_font(),16)
    text1=font.render('B=Tangtoc',True,trang)
    text1_rect=text1.get_rect()
    text1_rect.center=(450,200)
    manhinh.blit(text1,text1_rect)
    font2=pygame.font.Font(pygame.font.get_default_font(),16)
    text2=font.render('C=Giamtoc',True,trang)
    text2_rect=text2.get_rect()
    text2_rect.center=(450,250)
    manhinh.blit(text2,text2_rect)
    font3=pygame.font.Font(pygame.font.get_default_font(),16)
    text3=font.render('O=Dunglai',True,trang)
    text3_rect=text3.get_rect()
    text3_rect.center=(450,150)
    manhinh.blit(text3,text3_rect)
    font4=pygame.font.Font(pygame.font.get_default_font(),16)
    text4=font.render('P=Tieptuc',True,trang)
    text4_rect=text4.get_rect()
    text4_rect.center=(450,300)
    manhinh.blit(text4,text4_rect)
    if gameover:
        #đưa ra ô có muốn chơi lại k
        manhinh.blit(crash,crash_rect)
        pygame.draw.rect(manhinh,cam,(0,50,rong,100))
        font=pygame.font.Font(pygame.font.get_default_font(),16)
        text=font.render(f'Score:{diem}  Choi lai? (Y/N)',True,trang)
        text_rect=text.get_rect()
        text_rect.center=(250,100)
        manhinh.blit(text,text_rect)
    pygame.display.update()
    while gameover:
        clock.tick(fps)
        for event in pygame.event.get():
            if event.type==QUIT:
                gameover=False
                chaygame=False
            if event.type==KEYDOWN:
                if event.key==K_y:
                    #reset game , cài lại thôgn số cho game
                    gameover=False
                    diem=0
                    tocdo=2
                    chuongngaivat_group.empty()
                    Player.rect.center=[xe_x,xe_y]
                if event.key==K_n:
                    gameover=False
                    chaygame=False
pygame.quit
     