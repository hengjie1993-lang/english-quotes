# -*- coding: utf-8 -*-
"""
build_quotes.py — 生成 quotes.json

收录「经典公版英文名句 + 中文翻译」，作者限定去世超百年（公版领域），
翻译用自译或公版译本，版权干净。

字段：
  text      英文原句
  zh        中文翻译
  author    作者（公版名家，英文）
  authorZh  作者中文名（显示用）
  work      出处（作品名，留空表示无明确出处/传统归名）
  tags      主题标签，逗号分隔

运行：python build_quotes.py  -> 生成 quotes.json
"""
import json, os

ROOT = os.path.dirname(os.path.abspath(__file__))

# 作者中文名映射（按英文名查表）
AUTHOR_ZH = {
    "William Shakespeare": "莎士比亚",
    "Francis Bacon": "培根",
    "Socrates": "苏格拉底",
    "Plato": "柏拉图",
    "Aristotle": "亚里士多德",
    "Confucius": "孔子",
    "Lao Tzu": "老子",
    "Sun Tzu": "孙子",
    "Marcus Aurelius": "马可·奥勒留",
    "Seneca": "塞涅卡",
    "Cicero": "西塞罗",
    "Ralph Waldo Emerson": "爱默生",
    "Henry David Thoreau": "亨利·戴维·梭罗",
    "Benjamin Franklin": "富兰克林",
    "Abraham Lincoln": "亚伯拉罕·林肯",
    "Johann Wolfgang von Goethe": "歌德",
    "Friedrich Nietzsche": "尼采",
    "Mark Twain": "马克·吐温",
    "Oscar Wilde": "王尔德",
    "Victor Hugo": "维克多·雨果",
    "Leo Tolstoy": "列夫·托尔斯泰",
    "Fyodor Dostoevsky": "陀思妥耶夫斯基",
    "Rumi": "鲁米",
    "John Milton": "约翰·弥尔顿",
    "William Blake": "威廉·布莱克",
    "Percy Bysshe Shelley": "雪莱",
    "Walt Whitman": "沃尔特·惠特曼",
    "Emily Dickinson": "艾米莉·狄金森",
    "Robert Louis Stevenson": "史蒂文森",
    "George Eliot": "乔治·艾略特",
    "Thomas Carlyle": "托马斯·卡莱尔",
    "John Ruskin": "约翰·罗斯金",
    "Epicurus": "伊壁鸠鲁",
}

# [text, zh, author, work, tags]
DATA = [
    # ---------- William Shakespeare (1564-1616) ----------
    ["The fool doth think he is wise, but the wise man knows himself to be a fool.", "愚者自以为智，智者自知其愚。", "William Shakespeare", "As You Like It", "wisdom"],
    ["All the world's a stage, and all the men and women merely players.", "整个世界是个舞台，男男女女不过是演员。", "William Shakespeare", "As You Like It", "life"],
    ["To be, or not to be: that is the question.", "生存还是毁灭，这是一个值得思考的问题。", "William Shakespeare", "Hamlet", "life"],
    ["This above all: to thine own self be true.", "最重要的是：对自己要诚实。", "William Shakespeare", "Hamlet", "character"],
    ["Cowards die many times before their deaths; the valiant never taste of death but once.", "懦夫死前已死过多次，勇者一生只尝一次死亡。", "William Shakespeare", "Julius Caesar", "courage"],
    ["The fault, dear Brutus, is not in our stars, but in ourselves.", "布鲁图斯，错不在星宿，而在我们自己。", "William Shakespeare", "Julius Caesar", "character"],
    ["Men at some time are masters of their fates.", "人有时是命运的主宰。", "William Shakespeare", "Julius Caesar", "character"],
    ["Give every man thy ear, but few thy voice.", "多听少说。", "William Shakespeare", "Hamlet", "wisdom"],
    ["Brevity is the soul of wit.", "简洁是智慧的灵魂。", "William Shakespeare", "Hamlet", "wisdom"],
    ["There is nothing either good or bad, but thinking makes it so.", "没有绝对的善恶，是人的思想使然。", "William Shakespeare", "Hamlet", "wisdom"],
    ["What's done cannot be undone.", "木已成舟，无法挽回。", "William Shakespeare", "Macbeth", "wisdom"],
    ["Love looks not with the eyes, but with the mind.", "爱情不用眼睛，而用心灵去看。", "William Shakespeare", "A Midsummer Night's Dream", "love"],
    ["If music be the food of love, play on.", "倘若音乐是爱情的食粮，那就奏下去吧。", "William Shakespeare", "Twelfth Night", "love"],
    ["Parting is such sweet sorrow.", "离别是如此甜蜜的忧伤。", "William Shakespeare", "Romeo and Juliet", "love"],
    ["A rose by any other name would smell as sweet.", "玫瑰即使换名，也依然芬芳。", "William Shakespeare", "Romeo and Juliet", "love"],
    ["Our doubts are traitors, and make us lose the good we oft might win.", "我们的疑虑是叛徒，使我们错失本可赢得的好处。", "William Shakespeare", "Measure for Measure", "courage"],
    ["What's past is prologue.", "凡是过往，皆为序章。", "William Shakespeare", "The Tempest", "life"],
    ["When sorrows come, they come not single spies, but in battalions.", "忧患来袭，从不是单个探子，而是成群大军。", "William Shakespeare", "Hamlet", "life"],
    ["Some are born great, some achieve greatness, and some have greatness thrust upon them.", "有人生而伟大，有人成就伟大，有人被赋予伟大。", "William Shakespeare", "Twelfth Night", "success"],

    # ---------- Francis Bacon (1561-1626) ----------
    ["Knowledge is power.", "知识就是力量。", "Francis Bacon", "", "learning"],
    ["Reading maketh a full man; conference a ready man; and writing an exact man.", "读书使人充实，讨论使人机智，写作使人精确。", "Francis Bacon", "Of Studies", "learning"],
    ["Some books are to be tasted, others to be swallowed, and some few to be chewed and digested.", "有的书浅尝辄止，有的囫囵吞下，少数须咀嚼消化。", "Francis Bacon", "Of Studies", "learning"],
    ["A wise man will make more opportunities than he finds.", "智者创造的机会多于他所发现的。", "Francis Bacon", "", "success"],
    ["Studies serve for delight, for ornament, and for ability.", "读书足以怡情，足以傅彩，足以长才。", "Francis Bacon", "Of Studies", "learning"],
    ["Revenge is a kind of wild justice.", "复仇是一种野生的公道。", "Francis Bacon", "Of Revenge", "wisdom"],
    ["Whoever is delighted in solitude is either a wild beast or a god.", "喜独处者，非野兽即神灵。", "Francis Bacon", "Essays", "character"],
    ["Hope is a good breakfast, but it is a bad supper.", "希望是美味的早餐，却是糟糕的晚餐。", "Francis Bacon", "", "hope"],

    # ---------- William Shakespeare done; now Socrates / Plato ----------
    ["The unexamined life is not worth living.", "未经审视的人生不值得过。", "Socrates", "", "life"],
    ["The only true wisdom is in knowing you know nothing.", "唯一的真智慧，是知道自己一无所知。", "Socrates", "", "learning"],
    ["Education is the kindling of a flame, not the filling of a vessel.", "教育不是注满一桶水，而是点燃一把火。", "Socrates", "", "learning"],
    ["I know that I am intelligent, because I know that I know nothing.", "我知我智，因我知我之无知。", "Socrates", "", "learning"],
    ["We can easily forgive a child who is afraid of the dark; the real tragedy of life is when men are afraid of the light.", "我们易原谅怕黑的孩子；人生真正的悲剧，是成人害怕光明。", "Plato", "The Republic", "courage"],
    ["Wise men speak because they have something to say; fools because they have to say something.", "智者发言因有话要说，愚者发言因不得不说。", "Plato", "", "wisdom"],
    ["The beginning is the most important part of the work.", "开端是工作中最重要的部分。", "Plato", "", "success"],
    ["Necessity is the mother of invention.", "需要是发明之母。", "Plato", "", "success"],

    # ---------- Aristotle (384-322 BC) ----------
    ["We are what we repeatedly do. Excellence, then, is not an act, but a habit.", "我们重复做什么，便是什么人。卓越不是一时之举，而是一种习惯。", "Aristotle", "", "success"],
    ["Knowing yourself is the beginning of all wisdom.", "认识自己是一切智慧的开端。", "Aristotle", "", "wisdom"],
    ["Quality is not an act, it is a habit.", "品质不是一时之举，而是习惯。", "Aristotle", "", "character"],
    ["Patience is bitter, but its fruit is sweet.", "耐心苦涩，其果甘甜。", "Aristotle", "", "perseverance"],
    ["It is the mark of an educated mind to be able to entertain a thought without accepting it.", "受过教育者的标志，是能容纳一种思想而不必接受它。", "Aristotle", "", "learning"],
    ["Friendship is a single soul dwelling in two bodies.", "友谊是一个灵魂居于两个躯体。", "Aristotle", "", "friendship"],
    ["Courage is the first of human qualities because it is the quality which guarantees the others.", "勇气是人首要的品质，因为它保障其余品质。", "Aristotle", "", "courage"],

    # ---------- Confucius (551-479 BC) ----------
    ["It does not matter how slowly you go as long as you do not stop.", "只要不停下，走得慢也无妨。", "Confucius", "", "perseverance"],
    ["Learning without thought is labor lost; thought without learning is perilous.", "学而不思则罔，思而不学则殆。", "Confucius", "", "learning"],
    ["What you do not want done to yourself, do not do to others.", "己所不欲，勿施于人。", "Confucius", "", "character"],
    ["The superior man is modest in his speech but exceeds in his actions.", "君子讷于言而敏于行。", "Confucius", "", "character"],
    ["Real knowledge is to know the extent of one's ignorance.", "真正的知识，是知道自己无知的程度。", "Confucius", "", "learning"],
    ["Wherever you go, go with all your heart.", "无论去何处，都要全心全意。", "Confucius", "", "character"],
    ["To see what is right and not do it is want of courage.", "见义不为，是无勇也。", "Confucius", "", "courage"],
    ["He who learns but does not think is lost; he who thinks but does not learn is in danger.", "学而不思则罔，思而不学则殆。", "Confucius", "", "learning"],

    # ---------- Lao Tzu (6th century BC) ----------
    ["A journey of a thousand miles begins with a single step.", "千里之行，始于足下。", "Lao Tzu", "Tao Te Ching", "perseverance"],
    ["Nature does not hurry, yet everything is accomplished.", "自然从不匆忙，却成就万事。", "Lao Tzu", "Tao Te Ching", "nature"],
    ["Knowing others is intelligence; knowing yourself is true wisdom.", "知人者智，自知者明。", "Lao Tzu", "Tao Te Ching", "wisdom"],
    ["The soft overcomes the hard; the gentle overcomes the rigid.", "柔弱胜刚强。", "Lao Tzu", "Tao Te Ching", "wisdom"],
    ["When I let go of what I am, I become what I might be.", "当我放下所是，便成为所能是。", "Lao Tzu", "Tao Te Ching", "life"],
    ["Do the difficult things while they are easy and do the great things while they are small.", "难事于易时为之，大事于小时为之。", "Lao Tzu", "Tao Te Ching", "success"],
    ["Silence is a source of great strength.", "沉默是巨大的力量之源。", "Lao Tzu", "Tao Te Ching", "wisdom"],

    # ---------- Sun Tzu (6th century BC) ----------
    ["The supreme art of war is to subdue the enemy without fighting.", "不战而屈人之兵，善之善者也。", "Sun Tzu", "The Art of War", "wisdom"],
    ["Know the enemy and know yourself, and you need not fear the result of a hundred battles.", "知己知彼，百战不殆。", "Sun Tzu", "The Art of War", "wisdom"],
    ["Victorious warriors win first and then go to war, while defeated warriors go to war first and then seek to win.", "胜兵先胜而后求战，败兵先战而后求胜。", "Sun Tzu", "The Art of War", "success"],
    ["In the midst of chaos, there is also opportunity.", "乱中亦有机。", "Sun Tzu", "The Art of War", "success"],
    ["Opportunities multiply as they are seized.", "机遇在被把握时倍增。", "Sun Tzu", "The Art of War", "success"],

    # ---------- Marcus Aurelius (121-180) ----------
    ["You have power over your mind - not outside events. Realize this, and you will find strength.", "你掌控的是自己的心，而非外界之事。明白这点，你便有了力量。", "Marcus Aurelius", "Meditations", "character"],
    ["The happiness of your life depends upon the quality of your thoughts.", "你生活的幸福，取决于你思想的质量。", "Marcus Aurelius", "Meditations", "happiness"],
    ["Waste no more time arguing about what a good man should be. Be one.", "别再争论好人该是什么样，去做一个吧。", "Marcus Aurelius", "Meditations", "character"],
    ["The soul becomes dyed with the color of its thoughts.", "灵魂会染上思想的颜色。", "Marcus Aurelius", "Meditations", "character"],
    ["Very little is needed to make a happy life; it is all within yourself, in your way of thinking.", "幸福人生所需极少，全在于你自己的心境。", "Marcus Aurelius", "Meditations", "happiness"],
    ["If it is not right, do not do it; if it is not true, do not say it.", "若不正当，就别做；若不真实，就别说。", "Marcus Aurelius", "Meditations", "character"],
    ["Confine yourself to the present.", "把自己局限于当下。", "Marcus Aurelius", "Meditations", "life"],
    ["The impediment to action advances action. What stands in the way becomes the way.", "阻碍行动者，反促进行动；挡路之物，反成道路。", "Marcus Aurelius", "Meditations", "perseverance"],

    # ---------- Seneca (c. 4 BC - 65 AD) ----------
    ["It is not that we have a short time to live, but that we waste a lot of it.", "我们不是寿命短，而是浪费了太多。", "Seneca", "", "time"],
    ["Luck is what happens when preparation meets opportunity.", "运气，是准备遇上机会时的产物。", "Seneca", "", "success"],
    ["Every new beginning comes from some other beginning's end.", "每一个新的开始，都源自另一个开始的终结。", "Seneca", "", "life"],
    ["We suffer more often in imagination than in reality.", "我们常在想象中比在现实中受更多苦。", "Seneca", "", "wisdom"],
    ["He who is brave is free.", "勇敢者即自由人。", "Seneca", "", "freedom"],
    ["A gem cannot be polished without friction, nor a man perfected without trials.", "宝石不经摩擦不能发光，人不经磨难不能完善。", "Seneca", "", "perseverance"],
    ["While we wait for life, life passes.", "我们等待生活时，生活已悄然流逝。", "Seneca", "", "time"],

    # ---------- Cicero (106-43 BC) ----------
    ["Gratitude is not only the greatest of virtues, but the parent of all others.", "感恩不仅是最伟大的德性，更是其余一切之母。", "Cicero", "", "character"],
    ["A room without books is like a body without a soul.", "没有书的房间，犹如没有灵魂的躯体。", "Cicero", "", "learning"],
    ["While there's life, there's hope.", "一息若存，希望不灭。", "Cicero", "", "hope"],
    ["The life of the dead is placed in the memory of the living.", "逝者的生命，安放于生者的记忆中。", "Cicero", "", "life"],
    ["Friendship improves happiness and abates misery, by doubling our joy and dividing our grief.", "友谊增益欢乐、减轻悲哀，因它倍增喜悦、平分忧伤。", "Cicero", "", "friendship"],
    ["Justice is the virtue of the soul which gives to each his due.", "正义是灵魂之德，使人各得其所。", "Cicero", "", "character"],

    # ---------- Ralph Waldo Emerson (1803-1882) ----------
    ["What lies behind us and what lies before us are tiny matters compared to what lies within us.", "与我们内心之物相比，身后与眼前的一切都微不足道。", "Ralph Waldo Emerson", "", "character"],
    ["The only person you are destined to become is the person you decide to be.", "你注定成为的，是你决心成为的人。", "Ralph Waldo Emerson", "", "success"],
    ["Do not go where the path may lead, go instead where there is no path and leave a trail.", "不要走别人铺好的路，去没有路的地方，留下足迹。", "Ralph Waldo Emerson", "", "courage"],
    ["Our greatest glory is not in never falling, but in rising every time we fall.", "我们最大的荣耀不在于从未跌倒，而在于每次跌倒后都能站起。", "Ralph Waldo Emerson", "", "perseverance"],
    ["A hero is no braver than an ordinary man, but he is braver five minutes longer.", "英雄并不比常人更勇敢，只是多勇敢了五分钟。", "Ralph Waldo Emerson", "", "courage"],
    ["Write it on your heart that every day is the best day in the year.", "把「每一天都是一年中最好的一天」写在心上。", "Ralph Waldo Emerson", "", "happiness"],
    ["For every minute you are angry you lose sixty seconds of happiness.", "你每生气一分钟，就失去六十秒的幸福。", "Ralph Waldo Emerson", "", "happiness"],
    ["What you do speaks so loud that I cannot hear what you say.", "你的行动如此响亮，让我听不见你的言语。", "Ralph Waldo Emerson", "", "character"],
    ["Self-reliance is the only road to true freedom.", "自立是通往真正自由的唯一道路。", "Ralph Waldo Emerson", "", "freedom"],
    ["Nothing great was ever achieved without enthusiasm.", "没有热情，便无一伟大成就。", "Ralph Waldo Emerson", "", "success"],
    ["The purpose of life is not to be happy. It is to be useful, to be honorable, to be compassionate.", "生活的目的不是快乐，而是有所作为、有所尊荣、富有怜悯。", "Ralph Waldo Emerson", "", "life"],

    # ---------- Henry David Thoreau (1817-1862) ----------
    ["The mass of men lead lives of quiet desperation.", "大多数人过着平静的绝望生活。", "Henry David Thoreau", "Walden", "life"],
    ["Go confidently in the direction of your dreams. Live the life you have imagined.", "自信地朝梦想方向前进，去过你想象的生活。", "Henry David Thoreau", "Walden", "success"],
    ["Our life is frittered away by detail. Simplify, simplify.", "生活被琐碎消耗。简化，再简化。", "Henry David Thoreau", "Walden", "life"],
    ["All good things are wild and free.", "一切美好的事物都是野性而自由的。", "Henry David Thoreau", "Walking", "freedom"],
    ["Rather than love, than money, than fame, give me truth.", "比起爱、金钱、名声，我更渴望真理。", "Henry David Thoreau", "Walden", "truth"],
    ["Not until we are lost do we begin to understand ourselves.", "直到迷失，我们才开始了解自己。", "Henry David Thoreau", "Walden", "life"],
    ["The price of anything is the amount of life you exchange for it.", "任何事物的代价，是你用以交换的生命。", "Henry David Thoreau", "Walden", "life"],
    ["Live your beliefs and you can turn the world around.", "践行你的信念，你便能改变世界。", "Henry David Thoreau", "", "courage"],

    # ---------- Benjamin Franklin (1706-1790) ----------
    ["Well done is better than well said.", "做得好胜过说得好。", "Benjamin Franklin", "", "character"],
    ["Early to bed and early to rise makes a man healthy, wealthy, and wise.", "早睡早起使人健康、富裕又聪明。", "Benjamin Franklin", "", "life"],
    ["An investment in knowledge pays the best interest.", "对知识的投资，回报最丰厚。", "Benjamin Franklin", "", "learning"],
    ["By failing to prepare, you are preparing to fail.", "不准备，就是在准备失败。", "Benjamin Franklin", "", "success"],
    ["Tell me and I forget. Teach me and I remember. Involve me and I learn.", "告诉我，我会忘；教给我，我会记；让我参与，我才学会。", "Benjamin Franklin", "", "learning"],
    ["Lost time is never found again.", "失去的时间再也找不回来。", "Benjamin Franklin", "", "time"],
    ["Energy and persistence conquer all things.", "精力与毅力能征服一切。", "Benjamin Franklin", "", "perseverance"],
    ["Honesty is the best policy.", "诚实为上策。", "Benjamin Franklin", "", "character"],

    # ---------- Abraham Lincoln (1809-1865) ----------
    ["Nearly all men can stand adversity, but if you want to test a man's character, give him power.", "几乎所有人都经得起逆境，但要想考验一个人的品格，给他权力。", "Abraham Lincoln", "", "character"],
    ["Whatever you are, be a good one.", "无论你是什么，都要做个好样的。", "Abraham Lincoln", "", "character"],
    ["I walk slowly, but I never walk backward.", "我走得很慢，但从不后退。", "Abraham Lincoln", "", "perseverance"],
    ["Those who deny freedom to others deserve it not for themselves.", "剥夺他人自由的人，自己也不配享有自由。", "Abraham Lincoln", "", "freedom"],
    ["My great concern is not whether you have failed, but whether you are content with your failure.", "我担心的不是你失败，而是你安于失败。", "Abraham Lincoln", "", "perseverance"],
    ["Character is like a tree and reputation is its shadow.", "品格如树，声誉如影。", "Abraham Lincoln", "", "character"],
    ["You cannot escape the responsibility of tomorrow by evading it today.", "你无法用今天的逃避，躲开明天的责任。", "Abraham Lincoln", "", "character"],
    ["Most folks are about as happy as they make up their minds to be.", "大多数人的快乐程度，取决于他们下决心要快乐的程度。", "Abraham Lincoln", "", "happiness"],

    # ---------- Johann Wolfgang von Goethe (1749-1832) ----------
    ["Knowing is not enough; we must apply. Willing is not enough; we must do.", "知道不够，必须运用；意愿不够，必须行动。", "Johann Wolfgang von Goethe", "", "success"],
    ["Whatever you can do or dream you can, begin it. Boldness has genius, power and magic in it.", "无论你能做或梦想做何事，开始吧。胆识蕴含天赋、力量与魔力。", "Johann Wolfgang von Goethe", "", "courage"],
    ["The person who does not read good books has no advantage over the person who cannot read them.", "不读好书的人，并不比不识字的人占优势。", "Johann Wolfgang von Goethe", "", "learning"],
    ["Treat people as if they were what they ought to be and you help them become what they are capable of being.", "以他人应有的样子对待他，便助他成为所能成为的人。", "Johann Wolfgang von Goethe", "", "friendship"],
    ["As soon as you trust yourself, you will know how to live.", "一旦你相信自己，便知如何生活。", "Johann Wolfgang von Goethe", "", "character"],
    ["Things which matter most must never be at the mercy of things which matter least.", "最重要的事，绝不可受制于最不重要的事。", "Johann Wolfgang von Goethe", "", "wisdom"],
    ["He who enjoys doing and enjoys what he has done is happy.", "乐于做事并乐于所成之事者，是幸福的。", "Johann Wolfgang von Goethe", "", "happiness"],
    ["None are more hopelessly enslaved than those who falsely believe they are free.", "最无可救药被奴役的，是误以为自己自由的人。", "Johann Wolfgang von Goethe", "", "freedom"],

    # ---------- Friedrich Nietzsche (1844-1900) ----------
    ["That which does not kill us makes us stronger.", "凡杀不死我的，使我更强大。", "Friedrich Nietzsche", "", "perseverance"],
    ["He who has a why to live can bear almost any how.", "知晓为何而活的人，几乎能承受任何如何。", "Friedrich Nietzsche", "", "life"],
    ["Become who you are.", "成为你自己。", "Friedrich Nietzsche", "", "character"],
    ["When you gaze long into an abyss, the abyss also gazes into you.", "当你长久凝视深渊，深渊也凝视着你。", "Friedrich Nietzsche", "", "wisdom"],
    ["The higher we soar, the smaller we appear to those who cannot fly.", "我们飞得越高，在不能飞的人眼中就越小。", "Friedrich Nietzsche", "", "wisdom"],
    ["All truly great thoughts are conceived by walking.", "一切真正伟大的思想，皆于行走中孕育。", "Friedrich Nietzsche", "", "life"],
    ["Love your fate. It is your own.", "热爱你的命运，那是你自己的。", "Friedrich Nietzsche", "", "life"],

    # ---------- Mark Twain (1835-1910) ----------
    ["The two most important days in your life are the day you are born and the day you find out why.", "生命中最重要的两天，是你出生的那天，和你明白为何而生的那天。", "Mark Twain", "", "life"],
    ["Twenty years from now you will be more disappointed by the things that you didn't do than by the ones you did do.", "二十年后，让你失望的将不是你做过的事，而是你没做的事。", "Mark Twain", "", "life"],
    ["Kindness is the language which the deaf can hear and the blind can see.", "善良是聋者能听、盲者能见的语言。", "Mark Twain", "", "friendship"],
    ["Courage is resistance to fear, mastery of fear - not absence of fear.", "勇气是抵抗恐惧、驾驭恐惧，而非没有恐惧。", "Mark Twain", "", "courage"],
    ["The secret of getting ahead is getting started.", "领先的秘诀，在于开始。", "Mark Twain", "", "success"],
    ["Worry is like a rocking chair: it gives you something to do but gets you nowhere.", "忧虑如摇椅：让你有事做，却到不了任何地方。", "Mark Twain", "", "wisdom"],
    ["Keep away from people who try to belittle your ambitions.", "远离那些试图贬低你志向的人。", "Mark Twain", "", "friendship"],
    ["The best way to cheer yourself up is to try to cheer somebody else up.", "让自己开心的最好方法，是设法让别人开心。", "Mark Twain", "", "happiness"],
    ["Do the right thing. It will gratify some people and astonish the rest.", "做正确的事。这会取悦一些人，让其余人惊讶。", "Mark Twain", "", "character"],

    # ---------- Oscar Wilde (1854-1900) ----------
    ["Be yourself; everyone else is already taken.", "做你自己，因为别人都有人做了。", "Oscar Wilde", "", "character"],
    ["To live is the rarest thing in the world. Most people exist, that is all.", "生活是世上最稀罕的事，大多数人只是存在罢了。", "Oscar Wilde", "", "life"],
    ["We are all in the gutter, but some of us are looking at the stars.", "我们都在阴沟里，但有人仰望星空。", "Oscar Wilde", "", "hope"],
    ["The truth is rarely pure and never simple.", "真相很少纯粹，也从不简单。", "Oscar Wilde", "", "truth"],
    ["To love oneself is the beginning of a lifelong romance.", "爱自己，是一生浪漫之始。", "Oscar Wilde", "", "love"],
    ["A friend is one who knows you and loves you just the same.", "朋友是了解你、却依然爱你的人。", "Oscar Wilde", "", "friendship"],
    ["Experience is simply the name we give our mistakes.", "经验不过是我们给错误起的名字。", "Oscar Wilde", "", "wisdom"],
    ["Life is too important to be taken seriously.", "生命太重要，不该被认真对待。", "Oscar Wilde", "", "life"],

    # ---------- Victor Hugo (1802-1885) ----------
    ["Even the darkest night will end and the sun will rise.", "最黑暗的夜晚终会结束，太阳终将升起。", "Victor Hugo", "Les Misérables", "hope"],
    ["Nothing is more powerful than an idea whose time has come.", "没有什么比一个时机已到的思想更有力量。", "Victor Hugo", "", "success"],
    ["To love another person is to see the face of God.", "爱另一个人，就是看见神的面孔。", "Victor Hugo", "Les Misérables", "love"],
    ["He who opens a school door, closes a prison.", "开一扇校门，便关一扇牢门。", "Victor Hugo", "", "learning"],
    ["The greatest happiness of life is the conviction that we are loved.", "生命最大的幸福，是确信自己被爱着。", "Victor Hugo", "Les Misérables", "love"],
    ["Adversity makes men, and prosperity makes monsters.", "逆境造人，顺境造怪物。", "Victor Hugo", "", "perseverance"],
    ["There is nothing like a dream to create the future.", "没有什么比梦想更能创造未来。", "Victor Hugo", "", "hope"],
    ["Laughter is the sun that drives winter from the human face.", "笑声是驱散人脸上的冬天的太阳。", "Victor Hugo", "", "happiness"],

    # ---------- Leo Tolstoy (1828-1910) ----------
    ["Everyone thinks of changing the world, but no one thinks of changing himself.", "人人都想改变世界，却没人想改变自己。", "Leo Tolstoy", "", "character"],
    ["The two most powerful warriors are patience and time.", "最有力的两位战士，是耐心与时间。", "Leo Tolstoy", "", "perseverance"],
    ["If you want to be happy, be.", "若想快乐，就去快乐。", "Leo Tolstoy", "", "happiness"],
    ["We can know only that we know nothing. And that is the highest degree of human wisdom.", "我们仅知自己一无所知，而这正是人类智慧的最高境界。", "Leo Tolstoy", "", "learning"],
    ["The sole meaning of life is to serve humanity.", "生命的唯一意义，在于服务人类。", "Leo Tolstoy", "", "life"],
    ["Wrong does not cease to be wrong because the majority share in it.", "错误不因多数人的参与而变成正确。", "Leo Tolstoy", "", "character"],

    # ---------- Fyodor Dostoevsky (1821-1881) ----------
    ["The secret of man's being is not only to live but to have something to live for.", "人存在的秘密，不仅在于活着，更在于有所为而生。", "Fyodor Dostoevsky", "", "life"],
    ["To live without hope is to cease to live.", "没有希望地活着，便是停止生活。", "Fyodor Dostoevsky", "", "hope"],
    ["Beauty will save the world.", "美将拯救世界。", "Fyodor Dostoevsky", "", "truth"],
    ["Taking a new step, uttering a new word, is what people fear most.", "迈出一步、说出一个新词，是人们最恐惧的。", "Fyodor Dostoevsky", "", "courage"],
    ["We are all responsible for all.", "我们为一切负责。", "Fyodor Dostoevsky", "", "character"],

    # ---------- Rumi (1207-1273) ----------
    ["The wound is the place where the light enters you.", "伤口，是光照进你之处。", "Rumi", "", "perseverance"],
    ["What you seek is seeking you.", "你所寻觅的，也在寻觅你。", "Rumi", "", "life"],
    ["Raise your words, not your voice. It is rain that grows flowers, not thunder.", "提高言语，而非嗓门。催开花朵的是雨，不是雷。", "Rumi", "", "wisdom"],
    ["Yesterday I was clever, so I wanted to change the world. Today I am wise, so I am changing myself.", "昨日我聪慧，故想改变世界；今日我智慧，故改变自己。", "Rumi", "", "character"],
    ["Don't grieve. Anything you lose comes round in another form.", "不要悲伤，你失去的一切会以另一种形式归来。", "Rumi", "", "hope"],
    ["The only lasting beauty is the beauty of the heart.", "唯一恒久的美，是心灵之美。", "Rumi", "", "love"],

    # ---------- John Milton (1608-1674) ----------
    ["The mind is its own place, and in itself can make a heaven of hell, a hell of heaven.", "心是其自有之地，能化地狱为天堂，化天堂为地狱。", "John Milton", "Paradise Lost", "character"],
    ["Better to reign in hell than serve in heaven.", "宁在地狱为王，不在天堂为奴。", "John Milton", "Paradise Lost", "freedom"],
    ["They also serve who only stand and wait.", "那些伫立等候的人，也在服务。", "John Milton", "", "perseverance"],
    ["A good book is the precious lifeblood of a master spirit.", "好书是大师精神的宝贵血脉。", "John Milton", "", "learning"],

    # ---------- William Blake (1757-1827) ----------
    ["To see a world in a grain of sand, and a heaven in a wild flower.", "于一沙见世界，于一花见天堂。", "William Blake", "", "nature"],
    ["Energy is eternal delight.", "能量是永恒的喜悦。", "William Blake", "", "life"],
    ["No bird soars too high if he soars with his own wings.", "凭自己的翅膀高飞，没有鸟飞得太高。", "William Blake", "", "freedom"],
    ["What is now proved was once only imagined.", "今日已证之事，昔日为想象。", "William Blake", "", "success"],

    # ---------- Percy Bysshe Shelley (1792-1822) ----------
    ["If Winter comes, can Spring be far behind?", "冬天来了，春天还会远吗？", "Percy Bysshe Shelley", "Ode to the West Wind", "hope"],
    ["Fear not for the future, weep not for the past.", "不为将来惧，不为往昔泣。", "Percy Bysshe Shelley", "", "courage"],
    ["Love withers under constraint; its very essence is liberty.", "爱在束缚下凋萎，其本质正是自由。", "Percy Bysshe Shelley", "", "love"],
    ["Poetry is the record of the best and happiest moments of the best and happiest minds.", "诗歌是最美心灵最幸福时刻的记录。", "Percy Bysshe Shelley", "", "truth"],

    # ---------- Walt Whitman (1819-1892) ----------
    ["Keep your face always toward the sunshine - and shadows will fall behind you.", "永远面朝阳光，阴影便会落在身后。", "Walt Whitman", "", "hope"],
    ["The powerful play goes on, and you may contribute a verse.", "壮丽的戏剧继续上演，你也可献上一行诗。", "Walt Whitman", "Leaves of Grass", "life"],
    ["I am large, I contain multitudes.", "我胸怀广阔，我包罗万象。", "Walt Whitman", "Leaves of Grass", "character"],
    ["Re-examine all you have been told. Dismiss that which insults your soul.", "重审你听来的一切，抛弃那侮辱你灵魂之说。", "Walt Whitman", "", "character"],
    ["Rest is not quitting the fight. Rest is the part of the fight you're not yet strong enough to see.", "休息不是退出战斗，而是你尚未强大到能看清的战斗的一部分。", "Walt Whitman", "", "perseverance"],
    ["The earth is rude and incomprehensible at first; be not discouraged, keep on, there are divine things well enveloped.", "大地起初粗粝难解，别气馁，继续前行，神圣之物正被妥善包裹。", "Walt Whitman", "Leaves of Grass", "nature"],

    # ---------- Emily Dickinson (1830-1886) ----------
    ["Hope is the thing with feathers that perches in the soul.", "希望是栖于灵魂、生有羽毛之物。", "Emily Dickinson", "", "hope"],
    ["Forever is composed of nows.", "永远由无数个现在组成。", "Emily Dickinson", "", "life"],
    ["We never know how high we are till we are called to rise.", "不到被召唤奋起之时，我们不知自己能有多高。", "Emily Dickinson", "", "perseverance"],
    ["Dwell in possibility.", "栖居于可能之中。", "Emily Dickinson", "", "life"],
    ["Success is counted sweetest by those who ne'er succeed.", "成功之甘，未曾成功者尝得最浓。", "Emily Dickinson", "", "success"],
    ["Not knowing when the dawn will come, I open every door.", "不知黎明何时至，我敞开每一扇门。", "Emily Dickinson", "", "hope"],

    # ---------- Robert Louis Stevenson (1850-1894) ----------
    ["Don't judge each day by the harvest you reap but by the seeds you plant.", "勿以收成评判每一天，而以你播下的种子。", "Robert Louis Stevenson", "", "success"],
    ["Make the most of the best and the least of the worst.", "善处最佳，淡看最劣。", "Robert Louis Stevenson", "", "wisdom"],
    ["Keep your fears to yourself, but share your courage.", "恐惧留给自己，勇气与人分享。", "Robert Louis Stevenson", "", "courage"],
    ["To travel hopefully is a better thing than to arrive.", "怀抱希望地旅行，胜于抵达。", "Robert Louis Stevenson", "", "hope"],

    # ---------- George Eliot (1819-1880) ----------
    ["It is never too late to be what you might have been.", "成为你本可成为的人，永不为迟。", "George Eliot", "", "success"],
    ["What do we live for, if not to make life less difficult for each other?", "若不能让彼此生活稍易，我们活着何为？", "George Eliot", "", "friendship"],
    ["Blessed is the influence of one true, loving human soul on another.", "一个真诚、有爱之魂对另一个的影响，是蒙福的。", "George Eliot", "", "friendship"],
    ["Our sweetest songs are those that tell of saddest thought.", "我们最甜美的歌，诉说的是最哀伤的思绪。", "George Eliot", "", "life"],

    # ---------- Thomas Carlyle (1795-1881) ----------
    ["The man without a purpose is a ship without a rudder.", "没有目标的人，是缺舵之船。", "Thomas Carlyle", "", "success"],
    ["No pressure, no diamond.", "无压力，无钻石。", "Thomas Carlyle", "", "perseverance"],
    ["He who has health has hope; and he who has hope has everything.", "有健康者有希望；有希望者拥有一切。", "Thomas Carlyle", "", "hope"],
    ["Silence is the element in which great things fashion themselves together.", "沉默是伟大事物彼此成形的元素。", "Thomas Carlyle", "", "wisdom"],

    # ---------- John Ruskin (1819-1900) ----------
    ["The highest reward for a person's toil is not what they get for it, but what they become by it.", "劳作最高回报不在所得，而在所成。", "John Ruskin", "", "success"],
    ["Quality is never an accident. It is always the result of intelligent effort.", "品质从非偶然，必是明智努力之果。", "John Ruskin", "", "character"],
    ["When love and skill work together, expect a masterpiece.", "当爱与技巧携手，杰作可期。", "John Ruskin", "", "love"],
    ["The first wealth is health.", "健康是第一笔财富。", "John Ruskin", "", "life"],

    # ---------- Epicurus (341-270 BC) ----------
    ["It is not so much our friends' help that helps us, as the confidence of their help.", "与其说朋友的帮助助我们，不如说对他们会相助的信心助我们。", "Epicurus", "", "friendship"],
    ["The greater the difficulty, the more the glory in surmounting it.", "困难愈大，克服它的荣光愈盛。", "Epicurus", "", "perseverance"],
    ["Do not spoil what you have by desiring what you have not.", "别因觊觎未得之物，糟蹋了已有之物。", "Epicurus", "", "happiness"],
    ["Freedom is the oxygen of the soul.", "自由是灵魂之氧。", "Epicurus", "", "freedom"],
]


def main():
    out = []
    seen = set()
    for text, zh, author, work, tags in DATA:
        key = (text.strip().lower(), author.strip().lower())
        if key in seen:
            continue
        seen.add(key)
        a = author.strip()
        out.append({
            "id": len(out) + 1,
            "text": text.strip(),
            "zh": zh.strip(),
            "author": a,
            "authorZh": AUTHOR_ZH.get(a, a),
            "work": work.strip(),
            "tags": [t.strip() for t in tags.split(",") if t.strip()],
        })
    path = os.path.join(ROOT, "quotes.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    print(f"wrote {len(out)} quotes -> {path}")


if __name__ == "__main__":
    main()
