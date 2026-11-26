"""Warm red/cream native Kivy dashboard inspired by the supplied reference image.
All metrics are derived from actual saved study data; no fictional streaks/ranks.
"""
from kivy.metrics import dp, sp
from kivy.utils import get_color_from_hex as color
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.label import Label
from kivy.graphics import Color, RoundedRectangle

CREAM='#FCF8F5'; RED='#CB1830'; DARK_RED='#A40D25'; INK='#241D20'; MUTED='#8D8589'; WHITE='#FFFFFF'

def surface(widget, bg, radius=19):
    with widget.canvas.before:
        Color(*color(bg)); rect=RoundedRectangle(radius=[dp(radius)])
    def update(*_):rect.pos=widget.pos;rect.size=widget.size
    widget.bind(pos=update,size=update);update();return widget

def txt(value,size=15,fg=INK,height=None,align='left',bold=False):
    # Chinese font already registered by main.py
    w=Label(text=str(value),font_name='StudyFont',font_size=sp(size),bold=bold,color=color(fg),
            size_hint_y=None,height=dp(height or (size*1.7)),halign=align,valign='middle',shorten=True,shorten_from='right')
    w.bind(size=lambda widget,*_:setattr(widget,'text_size',(max(1,widget.width),widget.height)))
    return w

def panel(bg=WHITE,padding=14,radius=19):
    w=BoxLayout(orientation='vertical',spacing=dp(5),padding=dp(padding),size_hint_y=None)
    w.bind(minimum_height=w.setter('height'))
    return surface(w,bg,radius)

def tap(text, action, bg=WHITE,fg=INK, height=45, size=14):
    b=Button(text=text,font_name='StudyFont',font_size=sp(size),bold=True,size_hint_y=None,height=dp(height),
             background_normal='',background_down='',background_color=(0,0,0,0),color=color(fg))
    surface(b,bg,14);b.bind(on_release=lambda *_:action());return b

def stats_cell(value,name,emoji):
    card=panel();card.size_hint_y=1
    card.add_widget(txt(emoji,17,RED,23,'center'))
    card.add_widget(txt(value,21,INK,32,'center'))
    card.add_widget(txt(name,10,MUTED,22,'center'))
    return card

class FeatureCard(ButtonBehavior, BoxLayout):
    """Click-ready native card; no invisible button covering its labels."""
    def __init__(self, glyph, title, subtitle, action, accent, **kwargs):
        super().__init__(orientation='horizontal', spacing=dp(8),
                         padding=[dp(12), dp(10), dp(9), dp(10)],
                         size_hint_y=None, height=dp(116), **kwargs)
        surface(self, WHITE, 19)
        self.action = action
        icon_bg = BoxLayout(size_hint=(None, None), size=(dp(44), dp(44)),
                            padding=[dp(2), dp(2)])
        surface(icon_bg, accent[1], 12)
        icon_bg.add_widget(txt(glyph, 22, accent[0], 40, 'center', True))
        self.add_widget(icon_bg)
        texts = BoxLayout(orientation='vertical', spacing=dp(0))
        texts.add_widget(Widget())
        texts.add_widget(txt(title, 16, INK, 29, 'left', True))
        texts.add_widget(txt(subtitle, 10, MUTED, 27))
        texts.add_widget(Widget())
        self.add_widget(texts)

    def on_release(self):
        self.action()


def feature_card(icon, title, subtitle, action, accent):
    return FeatureCard(icon, title, subtitle, action, accent)

def navbar(app,active='home'):
    bar=BoxLayout(size_hint_y=None,height=dp(70),spacing=dp(3),padding=[dp(7),dp(7),dp(7),dp(9)])
    surface(bar,WHITE,0)
    actions=[('家','Trang chủ',app.show_home,'home'),('书','Bài học',app.show_levels,'lessons'),
             ('练','Luyện tập',app.open_dashboard_practice,'practice'),('我','Hồ sơ',app.show_profile,'profile')]
    for symbol,name,fn,key in actions:
        fg=RED if key==active else '#AAA1A4'
        btn=tap(symbol+'\n'+name,fn,WHITE,fg,54,12)
        btn.size_hint_y=1
        btn.halign='center'
        bar.add_widget(btn)
    return bar

def dashboard(app):
    from main import ROOT
    app.shell.clear_widgets();app.screen='home'
    outer=BoxLayout(orientation='vertical');surface(outer,CREAM,0);app.shell.add_widget(outer)
    scroll=ScrollView(do_scroll_x=False,bar_width=dp(3))
    body=BoxLayout(orientation='vertical',padding=[dp(18),dp(22),dp(18),dp(22)],spacing=dp(18),size_hint_y=None)
    body.bind(minimum_height=body.setter('height'));scroll.add_widget(body);outer.add_widget(scroll)
    header=BoxLayout(size_hint_y=None,height=dp(64),spacing=dp(10))
    avatar=tap('中',app.show_profile,RED,WHITE,60,23);avatar.size_hint_x=None;avatar.width=dp(62);header.add_widget(avatar)
    names=BoxLayout(orientation='vertical',spacing=dp(0));names.add_widget(txt('Xin chào 👋',13,MUTED,26));names.add_widget(txt('Học tiếng Trung',22,INK,36));header.add_widget(names)
    notif=tap('习',app.show_review,'#FFFFFF',RED,52,22);notif.size_hint_x=None;notif.width=dp(48);header.add_widget(notif)
    body.add_widget(header)
    lessons=app.lessons();best=app.study.get('best',{});done=sum(best.get(l['id'],0)>=60 for l in lessons)
    vocab=sum(app.vocab_key(e) in app.study.get('vocab',{}) for e in app.entries)
    total=len(lessons)+len(app.entries);pct=round(100*(done+vocab)/total) if total else 0
    points=sum(int(best.get(l['id'],0)) for l in lessons)+10*vocab
    row=BoxLayout(size_hint_y=None,height=dp(104),spacing=dp(8))
    for args in [(str(done+vocab),'Đã học','学'),(f'{points:,}'.replace(',','.'),'Điểm tích lũy','分'),(f'{pct}%','Tiến độ','%')]:row.add_widget(stats_cell(*args))
    body.add_widget(row)
    unfinished=next((l for l in lessons if best.get(l['id'],0)<60),lessons[0] if lessons else None)
    hero=panel(RED,19,26);hero.padding=[dp(19),dp(18),dp(19),dp(18)]
    top=BoxLayout(size_hint_y=None,height=dp(33))
    top.add_widget(txt('BÀI HỌC HÔM NAY',12,'#FFE8E8',28))
    badge=txt('NGỮ PHÁP',11,DARK_RED,28,'center');badge.size_hint_x=None;badge.width=dp(92);surface(badge,'#FFCB4E',16);top.add_widget(badge);hero.add_widget(top)
    hero.add_widget(txt(unfinished['hantu'] if unfinished else '你好',42,WHITE,73))
    hero.add_widget(txt(unfinished['title'] if unfinished else 'Bắt đầu hành trình',18,WHITE,39))
    hero.add_widget(txt('Hoàn thành một bài học mỗi ngày',12,'#FFDBDF',29))
    if unfinished:
        level=next((lv for lv in app.grammar['levels'] if unfinished in lv['lessons']),None)
        next_fn=lambda:app.show_lesson(unfinished,level)
    else:next_fn=app.show_levels
    action=tap('Tiếp tục học  →',next_fn,WHITE,DARK_RED,49,15);action.size_hint_x=None;action.width=dp(178);hero.add_widget(action)
    body.add_widget(hero)
    heading=BoxLayout(size_hint_y=None,height=dp(39));heading.add_widget(txt('Chủ đề học',21,INK,39));body.add_widget(heading)
    grid=GridLayout(cols=2,spacing=dp(12),size_hint_y=None,height=dp(244),row_force_default=True,row_default_height=dp(116))
    grid.add_widget(feature_card('词','Từ vựng',f'{len(app.entries)} từ · Học và ôn',app.show_vocabulary,('#BD6A22','#FFF0DE')))
    grid.add_widget(feature_card('音','Phát âm','Sắp ra mắt',app.open_pronunciation,('#7947B2','#F0E9FB')))
    grid.add_widget(feature_card('语','Ngữ pháp',f'{len(lessons)} cấu trúc',app.show_levels,('#168B7D','#E5FAF3')))
    grid.add_widget(feature_card('听','Luyện nghe','Sắp ra mắt',app.open_listening,('#B37A43','#FFF2E5')))
    body.add_widget(grid)
    wordheader=BoxLayout(size_hint_y=None,height=dp(33));wordheader.add_widget(txt('Từ vựng mới',21,INK,33));
    more=tap('Xem thêm',app.show_deck,CREAM,DARK_RED,30,12);more.size_hint_x=None;more.width=dp(92);wordheader.add_widget(more);body.add_widget(wordheader)
    words=BoxLayout(size_hint_y=None,height=dp(112),spacing=dp(9))
    for e in app.entries[:3]:
        c=panel(WHITE,9,15);c.size_hint_y=1
        c.add_widget(txt(e.hanzi,23,INK,37,'center'));c.add_widget(txt(e.pinyin,12,DARK_RED,25,'center'));c.add_widget(txt(e.meaning,11,MUTED,25,'center'));words.add_widget(c)
    body.add_widget(words)
    outer.add_widget(navbar(app,'home'))
