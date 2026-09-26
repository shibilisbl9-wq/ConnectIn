"""Build the October 2026 ConnectIn posts: HTML per slide, then PNG via Playwright (render.js).

Usage:  python3 build.py        # writes html/ and posts.json
        NODE_PATH=$(npm root -g) node render.js   # writes posts/<id>/<nn>.png

Images: drop the Higgsfield downloads into images/ with the names in IMAGES; any missing image
renders as a labelled placeholder panel so the layout can be reviewed before the photo arrives.
"""
import html
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
BRAND = '../../../brand'  # relative to html/
HEAD = f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><title>{{title}}</title>
<link rel="stylesheet" href="{BRAND}/samples/tokens.css">
<link rel="stylesheet" href="{BRAND}/components/bundle.css">
<link rel="stylesheet" href="../content.css">
<style>html,body{{margin:0;background:#fff}}</style></head><body>
'''
LOGO = (f'<img class="ci-logo ci-logo--standard" src="{BRAND}/assets/Logos/connectin-logo.png" alt="ConnectIn Business Services">'
        f'<img class="ci-logo ci-logo--reversed" src="{BRAND}/assets/Logos/connectin-logo-reversed.png" alt="ConnectIn Business Services">')

# Higgsfield jobs (nano_banana_pro, 2k, 4:5). File name in images/ -> job id + what it shows.
IMAGES = {
    'img-1-skyline.png': ('7e11b0f8-3623-41fb-b6c8-d00a19c27a6b', 'Dubai skyline in morning haze'),
    'img-2-fork.png': ('0c6a98d4-9e9b-48ac-a38f-cc38d4063ba3', 'Aerial highway splitting two ways'),
    'img-3-bank.png': ('43535652-991a-4dc0-a78b-704e981c6d82', 'Blank card and folder on marble, bank interior'),
    'img-4-scale.png': ('6ea14b77-2283-451d-a2bd-6954b68b639b', 'Brass balance scale with two white cubes'),
    'img-5-tower.png': ('ffedbe98-745e-4cb1-94cb-df41e191695c', 'Single glass office tower, pale sky'),
}
# Models: generated on a plain grey backdrop, cut out locally (fetch_images.py) to transparent PNGs.
MODELS = {
    'model-1-businessman.png': ('94e10a80-8c62-4b6e-951a-cf98d3d6aa83', 'Businessman in navy suit, walking, full length'),
    'model-2-emirati.png': ('5adb758c-e65a-48aa-a418-33eb0bc4e4bc', 'Emirati businessman in white kandura, full length'),
    'model-3-consultant.png': ('dd5a2ad8-62c3-43b8-b804-6be15f851381', 'Consultant in navy blazer and hijab, arms crossed'),
}

E = html.escape


def stack(lead, keyword, tag=None, gold=False, soft_tag=False, long=False):
    k = 'ci-keyword ci-keyword--gold' if gold else 'ci-keyword'
    k += ' ci-keyword--long' if long else ''
    t = ''
    if tag:
        t = f'<span class="ci-tag{" ci-tag--soft" if soft_tag else ""}">{E(tag)}</span>'
    return f'<div class="ci-stack"><p class="ci-lead">{E(lead)}</p><p class="{k}">{E(keyword)}</p>{t}</div>'


def pointer(text):
    return f'<p class="ci-pointer">{E(text)}</p>'


def pointers(items):
    return '<div class="ci-list">' + ''.join(pointer(i) for i in items) + '</div>'


def body(text):
    # **bold** support for the one line that matters
    parts = text.split('**')
    out = ''.join(f'<strong>{E(p)}</strong>' if i % 2 else E(p) for i, p in enumerate(parts))
    return f'<p class="ci-body">{out}</p>'


def title(text):
    # _word_ marks the one gold word
    parts = text.split('_')
    out = ''.join(f'<em>{E(p)}</em>' if i % 2 else E(p) for i, p in enumerate(parts))
    return f'<p class="ci-title">{out}</p>'


def fact(num, text):
    return f'<div class="ci-fact"><b>{E(num)}</b><span>{E(text)}</span></div>'


def warn(text):
    return f'<p class="ci-warn">{E(text)}</p>'


def source(text):
    return f'<p class="ci-source">{E(text)}</p>'


def numeral(n, gold=False):
    return f'<p class="ci-numeral{" ci-numeral--gold" if gold else ""}">{E(n)}</p><div class="ci-rule"></div>'


def compare(q_left, q_right, pick=None):
    cols = []
    for i, (h, p) in enumerate((q_left, q_right)):
        cls = 'ci-compare__col' + (' ci-compare__col--pick' if pick == i else '')
        cols.append(f'<div class="{cls}"><h3>{E(h)}</h3><p>{E(p)}</p></div>')
    return '<div class="ci-compare">' + ''.join(cols) + '</div>'


def table(head, rows):
    th = ''.join(f'<th>{E(h)}</th>' for h in head)
    tr = ''.join('<tr>' + ''.join(f'<td>{E(c)}</td>' for c in r) + '</tr>' for r in rows)
    return f'<table class="ci-table"><thead><tr>{th}</tr></thead><tbody>{tr}</tbody></table>'


def dates(rows):
    return '<div class="ci-dates">' + ''.join(
        f'<div class="ci-date"><span class="ci-tag">{E(d)}</span><p>{t}</p></div>' for d, t in rows) + '</div>'


def dm(word):
    return f'<div class="ci-dm"><span>DM us the word</span><b>{E(word)}</b></div>'


def image_panel(name):
    path = os.path.join(HERE, 'images', name)
    if os.path.exists(path):
        return f'<div class="ci-post__image"><img src="../images/{name}" alt=""></div>'
    job, what = IMAGES[name]
    return (f'<div class="ci-post__image ci-post__image--missing"><span>Image: {E(what)}<br>'
            f'{E(name)} · Higgsfield job {job[:8]}</span></div>')


SPLIT = '<!--split-->'
RULE = '<div class="ci-rule"></div>'


def arrange(main, inner):
    """Pick a layout: explicit split marker, numeral-on-top split, or vertically centred."""
    if SPLIT in main:
        top, bottom = main.split(SPLIT, 1)
    elif inner and main.startswith('<p class="ci-numeral') and RULE in main:
        i = main.index(RULE) + len(RULE)
        top, bottom = main[:i], main[i:]
    elif inner:
        return 'centerv', f'<div class="ci-group">{main}</div>'
    else:
        return None, main
    return 'split', f'<div class="ci-group ci-group--top">{top}</div><div class="ci-group">{bottom}</div>'


def model_layer(name, kind):
    path = os.path.join(HERE, 'images', name)
    cls = f'ci-post__model ci-post__model--{kind}'
    if os.path.exists(path):
        return f'<div class="{cls}"><img src="../images/{name}" alt=""></div>'
    job, what = MODELS[name]
    return (f'<div class="{cls} ci-post__model--missing"><span>Model cut-out: {E(what)}<br>'
            f'{E(name)} · job {job[:8]}</span></div>')


def slide(theme, head, main, foot_swipe=True, image=None, mist=False, tight=False, center=False, inner=False,
          model=None, model_kind='full'):
    cls = 'ci-post' + (' ci-post--mist' if mist else '') + (' ci-post--has-model' if model else '')
    attr = f' data-theme="{theme}"' if theme == 'navy' else ''
    layout, main = arrange(main, inner) if not image else (None, main)
    main_cls = ('ci-post__main' + (' ci-post__main--tight' if tight and not layout else '')
                + (f' ci-post__main--{layout}' if layout else '') + (' ci-post__main--inner' if inner else ''))
    img = (image_panel(image) if image else '') + (model_layer(model, model_kind) if model else '')
    swipe = '<span class="ci-swipe">Swipe</span>' if foot_swipe else ''
    return (f'<div class="{cls}"{attr}>\n<div class="ci-post__head">{head}</div>\n'
            f'<div class="{main_cls}">{main}</div>\n{img}\n'
            f'<div class="ci-post__foot"><span class="ci-post__url">connectin.ae</span>{swipe}</div>\n</div>')


def counter(i, n):
    return f'<p class="ci-label ci-counter">{i:02d} / {n:02d}</p>'


def cta(lead, keyword, text, word):
    return ('navy', LOGO, stack(lead, keyword, gold=True) + SPLIT + body(text) + dm(word))


# ---------------------------------------------------------------------------------------------
# The month. Each post: id, date, format, pillar, slides (theme, head, main, options), caption.
# Inner slides get a counter; the cover and closing slide carry the logo.
# ---------------------------------------------------------------------------------------------
POSTS = []


def post(pid, date, fmt, pillar, topic, slides, caption, alt):
    POSTS.append(dict(id=pid, date=date, format=fmt, pillar=pillar, topic=topic, slides=slides,
                      caption=caption, alt=alt))


HASH_SETUP = '#DubaiBusinessSetup #UAEBusiness #StartABusinessInDubai #DubaiEntrepreneurs #FreeZoneUAE #ConnectIn'
HASH_TAX = '#UAECorporateTax #UAEeInvoicing #FTA #DubaiSME #UAEBusiness #ConnectIn'

# P01 ---------------------------------------------------------------------------------------
post('P01', '2026-10-05', 'Carousel', 'Process', 'Four-week setup plan', [
    dict(theme='daylight', head=LOGO, mist=True, image='img-1-skyline.png', model='model-1-businessman.png',
         main=stack('Start in October, trade by', 'November', 'IN DUBAI') + pointer('Your four-week setup plan, week by week')),
    dict(theme='daylight', tight=True, main=numeral('01') + title('Week one: _decide_') +
         body('Pick your business activity, mainland or free zone, a trade name and who the shareholders are. **Every later step depends on these four answers.**')),
    dict(theme='daylight', tight=True, main=numeral('02') + title('Weeks one to two: the _licence_') +
         body('Initial approval, name reservation, company documents, then the licence itself. Most free zone licences are issued within a few working days once your documents are complete.')),
    dict(theme='daylight', tight=True, main=numeral('03') + title('Weeks two to three: _visas_') +
         body('Entry permit, medical test, Emirates ID biometrics, then the residence visa. Book the medical early: it is the step people forget to schedule.')),
    dict(theme='daylight', tight=True, main=numeral('04') + title('Weeks three to four: bank and _tax_') +
         body('Apply for the business bank account and register for corporate tax. New companies must register within 3 months of incorporation.') +
         warn('The bank account is usually the slowest step')),
    dict(theme='daylight', tight=True, main=title('Start the bank application the day your licence is _issued_') +
         body('Bank timelines vary from a couple of weeks to much longer, depending on the bank and your profile. Starting early is the one thing that reliably shortens it.')),
    dict(**dict(zip(('theme', 'head', 'main'), cta('Want the four weeks', 'Handled?',
         'We run the whole plan: licence, visas, bank introduction and tax registration, with one written timeline.', 'OCTOBER'))), last=True),
], caption=('Start in October, trade by November. Here is the four-week plan we use for a free zone setup, step by step.\n\n'
            'Save it for when you are ready, and send it to the co-founder who keeps asking "how long will it take?"\n\n'
            'Want it done for you? DM us "OCTOBER".\n\n' + HASH_SETUP),
   alt='Carousel: four-week Dubai company setup plan. Week one decide, weeks one to two licence, weeks two to three visas, weeks three to four bank account and corporate tax registration.')

# P02 ---------------------------------------------------------------------------------------
post('P02', '2026-10-07', 'Static', 'Compliance alert', 'E-invoicing ASP deadline', [
    dict(theme='navy', head=LOGO, main=stack('Revenue of AED 50M or more?', 'E-invoicing', 'ASP BY 30 OCT', gold=True) + SPLIT +
         body('Large businesses must appoint an Accredited Service Provider by 30 October 2026. Mandatory e-invoicing starts on 1 January 2027.') +
         fact('31 Mar 2027', 'ASP deadline for businesses below AED 50M'), last=True),
], caption=('E-invoicing is coming to the UAE, and the first deadline is this month.\n\n'
            'If your revenue is AED 50 million or more, you need an Accredited Service Provider (ASP) appointed by 30 October 2026. '
            'Mandatory e-invoicing for large businesses starts 1 January 2027. Everyone else: appoint by 31 March 2027, go live 1 July 2027.\n\n'
            'Not sure which group you are in? DM us "INVOICE" and we will check.\n\n' + HASH_TAX),
   alt='Navy post: revenue of AED 50 million or more, appoint an e-invoicing Accredited Service Provider by 30 October 2026. Mandatory e-invoicing starts 1 January 2027. Smaller businesses: ASP by 31 March 2027.')

# P03 ---------------------------------------------------------------------------------------
post('P03', '2026-10-08', 'Carousel', 'Decision guide', 'Mainland or free zone', [
    dict(theme='daylight', head=LOGO, mist=True, image='img-2-fork.png', model='model-2-emirati.png',
         main=stack('Mainland or', 'Free zone?', 'WHICH ONE FITS') + pointer('Four questions that settle it')),
    dict(theme='daylight', tight=True, main=title('Who are your _customers_?') +
         compare(('Mainland', 'You sell directly to customers anywhere in the UAE.'),
                 ('Free zone', 'You sell internationally, online, or to other free zone companies.'))),
    dict(theme='daylight', tight=True, main=title('Do you need a _shopfront_ or government contracts?') +
         compare(('Mainland', 'Yes: retail, restaurants and most government work need a mainland licence.'),
                 ('Free zone', 'No: you work from an office or flexi-desk inside the zone.'), pick=0)),
    dict(theme='daylight', tight=True, main=title('How much _space_ do you need?') +
         compare(('Mainland', 'A registered tenancy (Ejari) is normally required, and it sets your visa count.'),
                 ('Free zone', 'Flexi-desk packages are common, with a fixed number of visas included.'))),
    dict(theme='daylight', tight=True, main=title('What about _tax_?') +
         body('Both pay 9% corporate tax on profit above AED 375,000. A free zone company can get 0% on qualifying income, but only if it meets every condition. **It is not automatic.**')),
    dict(theme='daylight', tight=True, main=title('The short _answer_') +
         table(['If you…', 'Choose'], [['sell to UAE customers directly', 'Mainland'], ['sell abroad or online', 'Free zone'],
                                        ['need a shop or government work', 'Mainland'], ['want the lowest entry cost', 'Free zone, usually']])),
    dict(**dict(zip(('theme', 'head', 'main'), cta('Still between', 'The two?',
         'Tell us what you sell and to whom. We will recommend one, in writing, with the reasons.', 'CHOOSE'))), last=True),
], caption=('Mainland or free zone? It comes down to who your customers are and where you need to operate.\n\n'
            'Swipe through the four questions, then check the summary on slide 6. Save it before you speak to anyone about packages.\n\n'
            'Still unsure? DM us "CHOOSE" with what you sell and to whom.\n\n' + HASH_SETUP),
   alt='Carousel comparing mainland and free zone company setup in the UAE across customers, shopfront and government work, office space and visas, and corporate tax.')

# P04 ---------------------------------------------------------------------------------------
post('P04', '2026-10-12', 'Static', 'Checklist', 'Documents checklist', [
    dict(theme='daylight', head=LOGO, main=stack('Your setup', 'Checklist', 'FREE ZONE COMPANY') + SPLIT +
         pointers(['Passport copy for every shareholder, valid 6+ months', 'Passport photo on a white background',
                   'Visa or entry stamp copy, or Emirates ID if resident', 'No-objection letter if a UAE employer sponsors you',
                   'Business plan, for some activities']) +
         source('Typical list. Each free zone has its own requirements; we confirm yours before you apply.'), last=True),
], caption=('The documents you will be asked for, in one place. Save this and start collecting today: missing paperwork is the most common reason a setup stalls.\n\n'
            'Every authority has its own list, so treat this as the starting point. DM us "DOCS" and we will send the exact list for your free zone.\n\n' + HASH_SETUP),
   alt='Checklist post: documents for a free zone company setup. Passport copies, passport photo, visa or Emirates ID, no-objection letter if employed in the UAE, business plan for some activities.')

# P05 ---------------------------------------------------------------------------------------
post('P05', '2026-10-14', 'Carousel', 'Pain point', 'Opening a business bank account', [
    dict(theme='daylight', head=LOGO, mist=True, image='img-3-bank.png',
         main=stack('Opening a', 'Bank account?', 'FOR YOUR COMPANY', long=True) + pointer('What the bank will ask you for')),
    dict(theme='daylight', tight=True, main=title('The bank is checking one _thing_') +
         body('Is this a real business, run by real people, with clean money? Every document they ask for answers one part of that question.')),
    dict(theme='daylight', tight=True, main=title('Company _documents_') +
         pointers(['Trade licence and memorandum of association', 'Share certificate or register of shareholders',
                   'Passports and Emirates IDs of owners and signatories', 'Tenancy contract or flexi-desk agreement'])),
    dict(theme='daylight', tight=True, main=title('Proof the business is _real_') +
         pointers(['A short business plan: what you sell, to whom, where', 'Website or profile that matches your licence',
                   'Contracts, quotes or invoices if you have them', 'CVs of the owners'])),
    dict(theme='daylight', tight=True, main=title('Where the money comes _from_') +
         body('Expect to show personal bank statements and explain how the company is funded. **Round numbers with no story behind them slow everything down.**')),
    dict(theme='daylight', tight=True, main=title('The mistake that causes most _delays_') +
         body('Your licence activities, your business plan and what you tell the bank must describe the same business.') +
         warn('A mismatch means more questions, or a rejection')),
    dict(**dict(zip(('theme', 'head', 'main'), cta('Want the file', 'Bank-ready?',
         'We prepare your documents and introduce you to banks that fit your activity.', 'BANK'))), last=True),
], caption=('Opening a business bank account is where most new companies lose weeks. Here is what the bank is really checking, and what to have ready.\n\n'
            'Send this to your co-founder before the bank meeting.\n\n'
            'DM us "BANK" and we will review your file first.\n\n' + HASH_SETUP),
   alt='Carousel: documents UAE banks ask for when opening a business account, grouped into company documents, proof of business activity and source of funds.')

# P06 ---------------------------------------------------------------------------------------
post('P06', '2026-10-15', 'Static', 'Compliance alert', 'Corporate tax return due 31 Oct', [
    dict(theme='navy', head=LOGO, main=stack('Financial year ended 31 January?', 'Tax return', 'DUE 31 OCTOBER', gold=True) + SPLIT +
         body('Your corporate tax return and payment are due nine months after your year end. 31 October is a Saturday: file before the weekend, not on it.') +
         fact('AED 500', 'per month late-filing penalty, first 12 months'), last=True),
], caption=('Corporate tax reminder: if your financial year ended on 31 January 2026, your return and payment are due by 31 October 2026.\n\n'
            'The rule is nine months after your year end, for both filing and payment. Late filing costs AED 500 a month to start, and interest runs on unpaid tax.\n\n'
            'Year end on 31 March? You have until 31 December. Unsure of yours? DM us "TAX".\n\n' + HASH_TAX),
   alt='Navy post: financial year ended 31 January 2026, corporate tax return and payment due 31 October 2026. Late filing penalty from AED 500 per month.')

# P07 ---------------------------------------------------------------------------------------
post('P07', '2026-10-19', 'Carousel', 'Transparency', 'What a company really costs', [
    dict(theme='daylight', head=LOGO, mist=True, image='img-4-scale.png',
         main=stack('What does a company', 'Really cost?', 'IN DUBAI') + pointer('Every line item, before you compare packages')),
    dict(theme='daylight', tight=True, main=title('The package price is only the _start_') +
         body('Two quotes can look similar and end up thousands apart. The difference is always in what is left out. Here is the full list to check against.')),
    dict(theme='daylight', tight=True, main=numeral('01') + title('One-time _setup_') +
         pointers(['Licence and registration fees', 'Initial approval and name reservation', 'Establishment card (immigration file)'])),
    dict(theme='daylight', tight=True, main=numeral('02') + title('For every _visa_') +
         pointers(['Entry permit and change of status', 'Medical test', 'Emirates ID', 'Residence visa'])),
    dict(theme='daylight', tight=True, main=numeral('03') + title('Where you _work_') +
         pointers(['Flexi-desk, shared or private office', 'Tenancy registration (Ejari) on the mainland', 'More space usually means more visas'])),
    dict(theme='daylight', tight=True, main=numeral('04') + title('Every _year_ after') +
         pointers(['Licence renewal', 'Bookkeeping and corporate tax filing', 'Audit, where your zone requires it', 'VAT once you pass AED 375,000'])),
    dict(**dict(zip(('theme', 'head', 'main'), cta('Want every line', 'In writing?',
         'We send a line-by-line quote: government fees, visas, workspace and year-two costs.', 'COST'))), last=True),
], caption=('"From AED X" is never the whole story. Here is every cost of a Dubai company, grouped the way you will actually pay them.\n\n'
            'Save this and hold every quote against it, ours included.\n\n'
            'DM us "COST" for a line-by-line quote.\n\n' + HASH_SETUP),
   alt='Carousel listing the full costs of a Dubai company: one-time setup fees, per-visa costs, workspace, and annual costs such as renewal, bookkeeping, tax filing, audit and VAT.')

# P08 ---------------------------------------------------------------------------------------
post('P08', '2026-10-21', 'Static', 'Myth vs fact', 'Free zone does not mean zero tax', [
    dict(theme='daylight', head=LOGO, main=stack('Free zone means', 'Zero tax?', 'NOT ALWAYS') + SPLIT +
         body('Free zone companies are inside the UAE corporate tax system. The 0% rate applies only to qualifying income of a company that meets every condition, including real substance and audited accounts.') +
         body('**Everything else is taxed at 9% on profit above AED 375,000.**') +
         warn('Check before you promise investors 0%'), last=True),
], caption=('"Set up in a free zone and pay no tax." It is one of the most common assumptions, and it is only true in specific cases.\n\n'
            'The 0% rate is for qualifying income of a Qualifying Free Zone Person that meets every condition. Miss one and the standard 9% applies above AED 375,000 of profit.\n\n'
            'DM us "ZONE TAX" and we will tell you which side of the line you are on.\n\n' + HASH_TAX),
   alt='Myth versus fact post: free zone does not automatically mean zero tax. The 0% rate applies only to qualifying income when every condition is met; otherwise 9% applies above AED 375,000 of profit.')

# P09 ---------------------------------------------------------------------------------------
post('P09', '2026-10-22', 'Carousel', 'Process', 'First 90 days after the licence', [
    dict(theme='navy', head=LOGO, main=stack('Licence issued.', 'Now what?', 'YOUR FIRST 90 DAYS', gold=True) + SPLIT +
         '<p class="ci-numeral ci-numeral--gold">90</p>' + pointer('Five things to do before day 90')),
    dict(theme='daylight', tight=True, main=numeral('01') + title('Apply for the _bank_ account') +
         body('Start in week one. It is the slowest step and everything else, from paying rent to invoicing clients, waits on it.')),
    dict(theme='daylight', tight=True, main=numeral('02') + title('Register for corporate _tax_') +
         body('New companies must register with the Federal Tax Authority within 3 months of incorporation.') + fact('AED 10,000', 'penalty for late registration')),
    dict(theme='daylight', tight=True, main=numeral('03') + title('Watch the _VAT_ threshold') +
         body('Once taxable sales pass AED 375,000 over 12 months, you have 30 days to register for VAT. Track it monthly from the start.')),
    dict(theme='daylight', tight=True, main=numeral('04') + title('Finish your _visas_') +
         body('Residence visas and Emirates IDs for you and your team. Your visa quota depends on your workspace, so check it before you hire.')),
    dict(theme='daylight', tight=True, main=numeral('05') + title('Keep _records_ from day one') +
         body('Invoices, contracts and accounts must be kept for seven years. Set up bookkeeping now, not at year end.')),
    dict(**dict(zip(('theme', 'head', 'main'), cta('Want the 90 days', 'Covered?',
         'Bank, tax registration, visas and bookkeeping: one team, one checklist.', '90DAYS'))), last=True),
], caption=('Getting the licence feels like the finish line. It is the start of a 90-day checklist.\n\n'
            'Corporate tax registration within 3 months of incorporation (AED 10,000 if late), VAT once you pass AED 375,000, visas, bank and records. Save this.\n\n'
            'DM us "90DAYS" and we will run it with you.\n\n' + HASH_TAX),
   alt='Carousel: five things to do in the first 90 days after getting a UAE trade licence. Bank account, corporate tax registration within 3 months, VAT threshold of AED 375,000, visas, and seven-year record keeping.')

# P10 ---------------------------------------------------------------------------------------
post('P10', '2026-10-26', 'Carousel', 'Decision guide', 'Six questions before choosing a free zone', [
    dict(theme='daylight', head=LOGO, mist=True, image='img-5-tower.png',
         main=stack('Before you pick a', 'Free zone', 'ASK THESE 6') + pointer('The questions packages don\'t answer upfront')),
    dict(theme='daylight', tight=True, main=numeral('01') + title('Is my _activity_ on their list?') +
         body('Each free zone licenses its own set of activities. If yours is not listed, nothing else matters.')),
    dict(theme='daylight', tight=True, main=numeral('02') + title('How many _visas_ are included?') +
         body('And what does each extra visa cost? The answer often changes which package is cheapest.')),
    dict(theme='daylight', tight=True, main=numeral('03') + title('Is a _flexi-desk_ enough?') +
         body('Some activities or visa counts need a physical office. Find out before you sign for the desk.')),
    dict(theme='daylight', tight=True, main=numeral('04') + title('Is an annual _audit_ required?') +
         body('Some zones require audited accounts every year. It is a real cost, so put it in your budget now.')),
    dict(theme='daylight', tight=True, main=numeral('05') + title('Can I work with _mainland_ clients?') +
         body('Ask how, and what extra permit or structure it needs. It is a common surprise after setup.')),
    dict(theme='daylight', tight=True, main=numeral('06') + title('What does _year two_ cost?') +
         body('Renewal prices are not always the same as the first-year offer. Ask for the renewal quote in writing.')),
    dict(**dict(zip(('theme', 'head', 'main'), cta('Want us to ask', 'For you?',
         'We compare free zones against your activity, visas and budget, and show you the year-two numbers.', 'ZONE'))), last=True),
], caption=('Six questions to ask before you choose a free zone. The package price is the easy part; these are what decide whether it still works in year two.\n\n'
            'Save this for your shortlist calls.\n\n'
            'DM us "ZONE" and we will compare them for you.\n\n' + HASH_SETUP),
   alt='Carousel: six questions to ask before choosing a UAE free zone: permitted activities, visas included, flexi-desk or office, annual audit, mainland clients, and renewal cost.')

# P11 ---------------------------------------------------------------------------------------
post('P11', '2026-10-28', 'Static', 'Compliance alert', 'Deadlines to save', [
    dict(theme='navy', head=LOGO, main=stack('Save this:', 'Deadlines', 'OCT – DEC 2026', gold=True) + SPLIT +
         dates([('30 OCT', '<b>E-invoicing:</b> revenue AED 50M+ must appoint an ASP'),
                ('31 OCT', '<b>Corporate tax:</b> return and payment for years ended 31 January'),
                ('31 DEC', '<b>Corporate tax:</b> return and payment for years ended 31 March')]) +
         source('New company? Register for corporate tax within 3 months of incorporation.'), last=True),
], caption=('Three dates to put in the calendar now: 30 October, 31 October and 31 December.\n\n'
            'Save this post, and send it to whoever handles your company\'s filings.\n\n'
            'DM us "DEADLINES" and we will check which ones apply to you.\n\n' + HASH_TAX),
   alt='Navy post listing UAE deadlines: 30 October e-invoicing ASP appointment for revenue of AED 50 million or more; 31 October corporate tax for years ended 31 January; 31 December for years ended 31 March.')

# P12 ---------------------------------------------------------------------------------------
post('P12', '2026-10-29', 'Carousel', 'Trust', 'Five questions to ask any setup consultant', [
    dict(theme='daylight', head=LOGO, mist=True, model='model-3-consultant.png', model_kind='half',
         main=stack('Before you sign with any', 'Consultant', 'ASK THESE 5') + SPLIT +
         pointer('Including us. Especially us.') + body('A good consultant answers all five in writing, without hesitating.')),
    dict(theme='daylight', tight=True, main=numeral('01') + title('Is the quote _all-inclusive_?') +
         body('Government fees, visas, medical, Emirates ID and workspace. Ask what is not included, not just what is.')),
    dict(theme='daylight', tight=True, main=numeral('02') + title('Who _owns_ the documents?') +
         body('Your licence, company documents and portal logins should be in your name and in your hands.')),
    dict(theme='daylight', tight=True, main=numeral('03') + title('What if the _bank_ says no?') +
         body('Ask what they do next, and whether that is part of the fee.')),
    dict(theme='daylight', tight=True, main=numeral('04') + title('Who handles _year two_?') +
         body('Renewals, corporate tax filing and visa renewals. Setup is one month; running the company is every year after.')),
    dict(theme='daylight', tight=True, main=numeral('05') + title('Can I see a written _timeline_?') +
         body('Step by step, with who does what. If it is not written down, it is not a plan.')),
    dict(**dict(zip(('theme', 'head', 'main'), cta('Ask us', 'All five',
         'We will answer every question in writing before you pay anything.', 'ASK'))), last=True),
], caption=('Five questions to ask any business setup consultant before you sign. Including us.\n\n'
            'If the answers are vague, keep looking. Save this for your calls.\n\n'
            'DM us "ASK" and we will answer all five in writing.\n\n' + HASH_SETUP),
   alt='Carousel: five questions to ask a Dubai business setup consultant: is the quote all-inclusive, who owns the documents, what happens if the bank declines, who handles year two, and is there a written timeline.')


def build():
    os.makedirs(os.path.join(HERE, 'html'), exist_ok=True)
    manifest = []
    for p in POSTS:
        n = len(p['slides'])
        files = []
        for i, s in enumerate(p['slides'], 1):
            is_last = s.get('last', False) or i == n
            inner = not s.get('head')
            head = s.get('head') or counter(i, n)
            markup = slide(s['theme'], head, s['main'], foot_swipe=(not is_last and n > 1),
                           image=s.get('image'), mist=s.get('mist', False), tight=s.get('tight', False), inner=inner,
                           model=s.get('model'), model_kind=s.get('model_kind', 'full'))
            name = f"{p['id']}-{i:02d}.html"
            with open(os.path.join(HERE, 'html', name), 'w') as f:
                f.write(HEAD.replace('{title}', f"{p['id']} {i}/{n}") + markup + '\n</body></html>\n')
            files.append(name)
        manifest.append({k: p[k] for k in ('id', 'date', 'format', 'pillar', 'topic', 'caption', 'alt')} |
                        {'slides': files, 'images': sorted({s['image'] for s in p['slides'] if s.get('image')}),
                         'models': sorted({s['model'] for s in p['slides'] if s.get('model')})})
    with open(os.path.join(HERE, 'posts.json'), 'w') as f:
        json.dump({'images': IMAGES, 'models': MODELS, 'posts': manifest}, f, indent=2, ensure_ascii=False)
    write_calendar(manifest)
    print(len(POSTS), 'posts,', sum(len(p['slides']) for p in POSTS), 'slides')


def write_calendar(manifest):
    import datetime
    lines = ['# October 2026 calendar', '',
             'Generated by `build.py` from the same data as the slides. Edit copy in `build.py`, then rebuild.', '',
             '| Date | Post | Format | Pillar | Topic | Photo |', '| --- | --- | --- | --- | --- | --- |']
    for p in manifest:
        d = datetime.date.fromisoformat(p['date'])
        lines.append(f"| {d:%a %d %b} | {p['id']} | {p['format']} ({len(p['slides'])}) | {p['pillar']} | {p['topic']} | "
                     f"{', '.join(p['images'] + p['models']) or 'none: typographic'} |")
    for p in manifest:
        d = datetime.date.fromisoformat(p['date'])
        lines += ['', f"## {p['id']} · {d:%A %d %B} · {p['topic']}", '',
                  f"**{p['format']}**, {len(p['slides'])} slide{'s' if len(p['slides']) > 1 else ''} · pillar: {p['pillar']} · "
                  f"files: `posts/{p['id']}/01.png`" + (f" … `{len(p['slides']):02d}.png`" if len(p['slides']) > 1 else ''), '',
                  '**Caption**', '', '```', p['caption'], '```', '', f"**Alt text:** {p['alt']}"]
        if p['images']:
            lines += ['', '**Photo:** ' + '; '.join(f"`{i}`: {IMAGES[i][1]} (Higgsfield job `{IMAGES[i][0]}`)" for i in p['images'])]
        if p['models']:
            lines += ['', '**Model:** ' + '; '.join(f"`{m}`: {MODELS[m][1]} (Higgsfield job `{MODELS[m][0]}`)" for m in p['models'])]
    with open(os.path.join(HERE, 'calendar.md'), 'w') as f:
        f.write('\n'.join(lines) + '\n')


if __name__ == '__main__':
    build()
