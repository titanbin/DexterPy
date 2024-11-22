import pygame,pymupdf,os,pygame_textinput,sys
import numpy as np

def setup(filename,page_num=0):
    if ".pdf" in filename:
        pdf_path = "test.pdf"
        doc = pymupdf.open(pdf_path)
        page = doc.load_page(page_num)
        image = page.get_pixmap(dpi=500)
        if image.width/1920 > image.height/1080:
            if image.width > 1500:
                image = page.get_pixmap(dpi=int(500*1500/image.width))
        else:
            if image.height > 800:
                image = page.get_pixmap(dpi=int(500*800/image.height))
    
        mode = "RGB" if image.n >= 3 else "P"

        os.environ['SDL_VIDEO_CENTERED'] = '1'
        pygame.init()

        #pygame.display.set_mode((image.width, image.height))
        pygame.display.set_caption("Dexter.py")

        img = pygame.image.fromstring(image.samples, (image.width, image.height), mode)
        doc.close()

    elif '.png' in filename or '.jpg' in filename:
        img = pygame.image.load(filename)
        w,h = img.get_width(),img.get_height()
        if w/1920 > h/1080:
            if w > 1500:
                img = pygame.transform.scale(img,(1500,int(1500*h/w)))
            elif w < 1000:
                img = pygame.transform.scale(img,(1000,int(1000*h/w)))
        else:
            img = pygame.transform.scale(img,(int(800*w/h),800))
        os.environ['SDL_VIDEO_CENTERED'] = '1'
        pygame.init()

        pygame.display.set_caption("Dexter.py")
    
    window = pygame.display.set_mode((img.get_width(), img.get_height() + 60), pygame.RESIZABLE)

    return window,img

def draw_zoom():
    mx,my = pygame.mouse.get_pos()
    zoom_surface.blit(image,(0,0),(mx-25,my-25,50,50))
    pygame.draw.line(zoom_surface,(255,0,0),(25,0),(25,50))
    pygame.draw.line(zoom_surface,(255,0,0),(0,25),(50,25))
    pygame.draw.rect(zoom_surface,(0,0,0),(0,0,50,50),1)
    zoom_x = mx + 10
    zoom_y = my + 10
    if mx > window.get_width()-100:
        zoom_x = mx-110
    if my > window.get_height()-60:
        return
    if my > window.get_height()-160:
        zoom_y = my-110
    window.blit(pygame.transform.scale(zoom_surface,(100,100)),(zoom_x,zoom_y))

def render_toolbar(active_tool):
    toolbar_surf = pygame.Surface((window.get_width(),60))
    pygame.draw.rect(toolbar_surf,(150,150,150),(0,0,window.get_width(),60))
    pygame.draw.line(toolbar_surf,(0,0,0),(0,0),(window.get_width(),0),width=2)
    
    if False:
        for i in range(3):
            button_surf = pygame.Surface((50,50))
            mult = 1
            if active_tool == i:
                mult = .75
            pygame.draw.rect(button_surf,(175*mult,175*mult,175*mult),(0,0,50,50))
            pygame.draw.rect(button_surf,(0,0,0)      ,(0,0,50,50),width=1)
            if i == 0:
                pygame.draw.line(button_surf,(255*mult,0,0),(50/2,5),(50/2,45),width=3)
                pygame.draw.line(button_surf,(255*mult,0,0),(50/2-5, 5),(50/2+5, 5),width=3)
                pygame.draw.line(button_surf,(255*mult,0,0),(50/2-5,45),(50/2+5,45),width=3)
            elif i == 1:
                pygame.draw.line(button_surf,(0,0,255*mult),(5,50/2),(45,50/2),width=3)
                pygame.draw.line(button_surf,(0,0,255*mult),( 5,50/2-5),( 5,50/2+5),width=3)
                pygame.draw.line(button_surf,(0,0,255*mult),(45,50/2-5),(45,50/2+5),width=3)
            elif i == 2:
                pygame.draw.line(button_surf,(0,255*mult,0),(5,50/2),(45,50/2),width=3)
                pygame.draw.line(button_surf,(0,255*mult,0),(50/2,5),(50/2,45),width=3)
            toolbar_surf.blit(button_surf,(5 + i*55,5))

    for i in range(4):
        textinput = textinputs[i]
        pygame.draw.rect(toolbar_surf,(200,200,200),(30+i*100,15,70,30))
        pygame.draw.rect(toolbar_surf,(0,0,0),(30+i*100,15,70,30),width=1)

    return toolbar_surf


def render_textinputs():
    second_toolbar.fill((0,0,0,0))
    for i in range(4):
        txt = pygame.font.Font.render(font,('x0','x1','y0','y1')[i],True,(0,0,0))
        rect = txt.get_rect()
        rect.centerx = 5 + i*100 + rect.w / 2
        rect.centery = 20    + rect.h / 2
        second_toolbar.blit(txt,rect)
        second_toolbar.blit(textinputs[i].surface, (35+i*100,20))
    window.blit(second_toolbar,(0,window.get_height()-60))

def use_tool(x0,y0,x1,y1):
    global hx_0,hy_0,hx_1,hy_1,vx_0,vy_0,vx_1,vy_1,data
    d = np.sqrt((x1-x0)**2 + (y1-y0)**2)
    if d > 10:
        if np.abs(x1-x0) > np.abs(y1-y0):
            hx_0,hy_0 = x0,y0
            hx_1,hy_1 = x1,y0
        else:
            vx_0,vy_0 = x0,y0
            vx_1,vy_1 = x0,y1
    else:
        is_on_point = False
        for point in data:
            if np.sqrt((point[0]-x0)**2 + (point[1]-y0)**2) < 10:
                data.remove(point)
                is_on_point = True
                break
        if not is_on_point:
            data.append((x1,y1))

def render_gui(md,x0,y0,x1,y1):
    pygame.draw.line(window,(255,0,0),(hx_0,hy_0),(hx_1,hy_1),width=3)
    pygame.draw.line(window,(0,0,255),(vx_0,vy_0),(vx_1,vy_1),width=3)
    if md:
        d = np.sqrt((x1-x0)**2 + (y1-y0)**2)
        if d > 10:
            if np.abs(x1-x0) > np.abs(y1-y0):
                col = (255,0,0)
            else:
                col = (0,0,255)
            pygame.draw.line(window,col,(x0,y0),(x1,y1),width=3)
    for point in data:
        pygame.draw.line(window,(0,255,0),(point[0]-5,point[1]),(point[0]+5,point[1]),width=3)
        pygame.draw.line(window,(0,255,0),(point[0],point[1]-5),(point[0],point[1]+5),width=3)

def validate_text_input(text):
    if "\t" in text:
        return False
    if " " in text:
        return False
    if len(text) > 5:
        return False
    if text == '-' or text == "":
        return True
    try:
        int(text)
        return True
    except:
        return False

def handle_cursor():
    mx,my = pygame.mouse.get_pos()
    is_on_textinput = -1
    if my < window.get_height()-60:
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_CROSSHAIR)
    else:
        for i in range(4):
            textinput = textinputs[i].surface.get_rect()
            textinput.x = 30+i*100
            textinput.y = window.get_height()-60+15
            textinput.w = 70
            textinput.h = 30
            if textinput.collidepoint(mx,my):
                is_on_textinput = i
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_IBEAM)
                return is_on_textinput
        if is_on_textinput == -1:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
        
    return is_on_textinput

def compute_data():
    px_0,px_1 = min(hx_0,hx_1),max(hx_0,hx_1)
    py_0,py_1 = max(vy_0,vy_1),min(vy_0,vy_1)
    x_0,x_1 = min(int(textinputs[0].value),int(textinputs[1].value)),max(int(textinputs[0].value),int(textinputs[1].value))
    y_0,y_1 = min(int(textinputs[2].value),int(textinputs[3].value)),max(int(textinputs[2].value),int(textinputs[3].value))
    a_h = (x_1-x_0)/(px_1-px_0)
    b_h = x_0 - a_h*px_0
    a_v = (y_1-y_0)/(py_1-py_0)
    b_v = y_0 - a_v*py_0
    list_data = []
    for point in data:
        x = point[0]
        y = point[1]
        if logged[0]:
            x_ = 10**(np.log10(x_0) + (x-px_0)/(px_1-px_0)*(np.log10(x_1)-np.log10(x_0)))
        else:
            x_ = a_h*x + b_h
        if logged[1]:
            y_ = 10**(np.log10(y_0) + (y-py_0)/(py_1-py_0)*(np.log10(y_1)-np.log10(y_0)))
        else:
            y_ = a_v*y + b_v
        list_data.append((x_,y_))
    print(list_data)

active_tool = -1

window,image = setup(sys.argv[1])
logged = (False,False)

clock = pygame.time.Clock()
font = pygame.font.SysFont("Consolas", 20)
textinputs = []
for i in range(4):
    manager = pygame_textinput.TextInputManager(validator = validate_text_input)
    textinput = pygame_textinput.TextInputVisualizer(manager=manager,font_object=font)
    textinputs.append(textinput)
active_textinput = 0
toolbar = render_toolbar(active_tool)
second_toolbar = pygame.Surface((toolbar.get_width(),toolbar.get_height()))
second_toolbar = second_toolbar.convert_alpha()
zoom_surface = pygame.Surface((50,50))
dragging = False
mx_0,my_0 = -1,-1
mx_1,my_1 = -1,-1
hx_0,hy_0 = -1,-1
hx_1,hy_1 = -1,-1
vx_0,vy_0 = -1,-1
vx_1,vy_1 = -1,-1
data = []

# Event loop
running = True
while running:
    rerender = False
    events = pygame.event.get()
    on_textinput = handle_cursor()
    for event in events:
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.TEXTINPUT:
            if (event.text == '&' or event.text == '1') and active_tool != 0:
                active_tool = 0
            if (event.text == 'é' or event.text == '2') and active_tool != 1:
                active_tool = 1
            if (event.text == '"' or event.text == '3') and active_tool != 2:
                active_tool = 2
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RETURN:
                compute_data()
            if event.key == pygame.K_TAB:
                if pygame.key.get_mods() & pygame.KMOD_SHIFT:
                    active_textinput -= 1
                else:
                    active_textinput += 1
                for i in range(4):
                    textinputs[i].cursor_width = 0
                active_textinput = active_textinput % 4
                textinputs[active_textinput].cursor_width = 2
        if event.type == pygame.KEYDOWN:
            rerender = True
        if event.type == pygame.MOUSEBUTTONDOWN:
            dragging = True
            mx_0,my_0 = pygame.mouse.get_pos()
        if event.type == pygame.MOUSEBUTTONUP:
            if on_textinput != -1:
                active_textinput = on_textinput
                for i in range(4):
                    textinputs[i].cursor_width = 0
                textinputs[active_textinput].cursor_width = 2
            if dragging:
                dragging = False
                mx_1,my_1 = pygame.mouse.get_pos()
                use_tool(mx_0,my_0,mx_1,my_1)

    window.blit(image,(0, 0))
    textinputs[active_textinput].update(events)
    if rerender:
        toolbar = render_toolbar(active_tool)
    render_gui(pygame.mouse.get_pressed(num_buttons=3)[0],mx_0,my_0,pygame.mouse.get_pos()[0],pygame.mouse.get_pos()[1])
    window.blit(toolbar,(0,window.get_height()-60))
    render_textinputs()
    draw_zoom()
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()