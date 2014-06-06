'''
Created on Feb 21, 2014

@author: Renmiri
'''
import urllib.request
import xml.etree.ElementTree as ET
import PIL
from PIL import Image
from PIL import ImageChops
import math, operator
import hashlib
import os
from io import BytesIO

def get_owner():
    tree = ET.parse('ownerdata.xml')
    root = tree.getroot()
    for odata in root:
        print("reading",odata.tag)
        if odata.tag == 'scroll':
            thescroll = odata.get("name")
            print(odata.tag," = ",thescroll)
        return thescroll


def get_unkbreed_dict():
    tree = ET.parse('breedlist_'+thescroll+'.xml')
    root = tree.getroot()
    breed_dict = {}
    for breed in root:
        path = breed.text.replace("http://dragcave.net","")
        breed1 = breed.get('id')
        stage = ""
        gender = ""
        breed_dict[path] = breed1
        #print("..",path,breed1,stage,gender)

    print("done reading unknown")
    return(breed_dict)

def read_dragons():
    try:
        tree = ET.parse('breedids'+thescroll+'.xml')
    except:
        tree = ET.fromstring('<?xml version="1.0"?><data><breedid name="/images/gtMN.png"><path>/images/gtMN.png</path><imgtoid>http://dragcave.net/images/gtMN.png</imgtoid><matchid>Horse.png</matchid><found>True</found><rms>0.0</rms></breedid></data>')
        tree = ET.ElementTree(tree)
    root = tree.getroot()
    breed_dict = {}
    for breed in root:
        path = breed.find('path').text
        breed1 = breed.find('imgtoid').text
        result = breed.find('found').text
        match = breed.find('matchid').text
        rms = breed.find('rms').text
        breed_dict[path] = match
        print(path,breed1,result,match,rms)
    print("done reading known")
    return(breed_dict,breed_dict)


def load_saved_imgs():
    #imglist = "2headedfemale.gif 2headedfemales2.gif 2headedmale.gif 2headeds1.gif 2headed_male_hatchie.png 2headegg.gif 2lindhwurmaltf.png 2lindhwurmaltm.png 2lindhwurm_f.png 2lindhwurm_m.png Albinos1.gif Albinos2.gif albinos3.gif Albino_Egg.gif Autumn_Leetle_Tree.gif balloons1.gif balloons3.gif Balloon_egg.gif Balloon_s2.gif Blackalt3female.gif Blackalt3male.gif Blackalt_curlyf2b.gif Blackalt_curly_1st.gif Blackalt_sit_1st.gif Blackalt__sit_2nd.gif blackteaf.png blackteam.png blackteas1.gif blackteas2.gif blacktip.png blacktipegg.gif blacktips1.gif Blacktips2.gif Black_Egg.gif black_f.gif Black_hatchies1.png Black_hatchies2f.gif Black_hatchies2m.png black_m.gif Bloodmoon.gif bloodmoonf.png bloodmoonm.png bloodmoons1.gif bloodmoons2.png bloodscalef.png bloodscalem.png blunaegg.gif Blunaf.png blunas1.gif blunas2.gif Bluna_Male_.gif blusangf.png blusangm.png BrightBreasted_egg.gif BrightBreasted_males2.gif BrightBreasted_s1.gif BrightBreasted_s2.gif BrightBreasted_s3f.gif BrightBreasted_s3m.gif BrightPink3.gif BrightPinkegg.gif Brightpink_s2.gif BrightPlinks1.gif brimstone.png brimstones1.png brimstones2.png Canopyegg.gif canopys1.gif canopys2a.gif canopys3f.png canopys3male.gif Canopy_f.png Cheese_.gif Cheese_Adult.gif Cheese_egg.gif Cheese_s2.gif Chick.gif Chicken_Adult.gif Chicken_Egg.gif chr1_Holly_Egg_2010.png chr1_Holy.gif chr1_Holys1.gif chr1_Holys2.gif chr1_Yule.gif chr1_Yuleegg.gif chr1_Yules1.gif chr1_yules2.gif chr2_Snowangelegg.gif chr2_Snowangelgold.gif chr2_snowangels1.gif chr2_Snowangels2.gif chr2_snowangeltricolor.png chr2_snowangelwhite.png chr3_ribbon.png chr3_ribbonegg.png chr3_RibbonS2.png chr3_Ribon_Dancer_S1.png chr4_Wintermagi.gif chr4_WinterMagi.png chr4_wintermagis1.png chr4_Wintermagis2.png chr5_WrappingWing.png chr5_wrappingwings1.png chr5_wrappingwings2.png chr6_solstice.png coastalegg.gif Coastals1.gif Coastals2.gif coastals3.png copperbrownf.png copperbrownm.png copperbrowns2m.png coppergreenf.png coppergreenm.png coppergreens2f.png coppergreens2m.png copperredegg.png copperredf.png copperredm.png copperreds2f.png darkg_VineAlt.gif darkg_Vinealt_1st_stage.gif darkg_Vinealt_2nd_stage_Hatchling.gif darkg_Vine_Adult.gif darkg_Vine_egg.gif darkg_Vine_Hatchling.gif darkg_Vine_s1.gif daydeams1.gif daydreams2b.gif daydreams3f.gif daydreamsmale.png Daydream_Egg.gif Deepseas2.gif deepseas3.gif deepses1.gif Deep_sea_Egg.gif Dorsal-purple-egg-new.gif Dorsal.png Dorsalalt.gif Dorsalaltegg.gif Dorsalalts1.gif Dorsals1.gif dorsals2.gif Dorsaps2b.gif duotone.png duotone1.png duotoneegg.png duotones1.png Earth-day_tree.png Electrics1.gif electrics2m.gif electrics3f.gif electrics3m.gif Electric_Egg.gif Emberegg.gif EmberFemale.png Embermale.png embers1.gif Embers2.gif flamingoegg.gif flamingofemales2.gif flamingomales2.gif Flamingos1.gif flamingos3f.gif flamingos3m.gif fleshcrown1.png fleshcrown2.png fleshcrowns1.gif fleshcrowns2.png Frill3.gif Frilled_Hatchling_.gif Frilled_Hatchling_S2_.gif Frill_Egg.gif geode.gif Geode3.gif Geodeegg.gif Geode_Hatchling_S1_.gif Geode_Hatchling_S2.gif glo_Dayglory.gif glo_Dayglorys1.gif glo_dayglorys2.png glo_Dayglory_egg.gif glo_Nightglory.gif glo_nightglorys1.gif glo_nightglorys2.png Goldfish.gif goldfishs1.gif goldfishs2a.gif goldfishs2b.gif GoldfishShallowwaterfemale.png GoldfishShalowatermale.png Gold_Update.gif Gold_UpdateEgg.gif Gold_Update_Female.gif Gold_Update_male.png Gold_Update_s2f.gif Gold_Update_s2m.gif Gray.gif Grayegg.gif Gray_Adult.gif Gray_Hatchling.gif Gray_s2.gif Greenwing.png Greenwingegg.gif greenwings1.gif greenwings2.gif green_Earthquakeegg.gif green_Earthquake_Adult.gif green_Earthquake_Hatchling.gif green_Earthquake_s2.gif Guardian3.gif Guardianegg.gif Guardian_-_Hatchling.gif Guardian_s2.gif guoldenwyvern1.png guoldenwyvern2.png h0_pumpkins1.gif h0_pumpkins2.gif h0_Pumpkin_Adult.gif h0_Pumpkin_egg.gif h1_Marrowegg.gif h1_MarrowF.gif h1_Marrowmale.gif h1_marrows1.gif h1_Marrows2.gif h2_shadowwalkeregg.gif h2_shadowwalkers1.png h2_ShadowWalkers2.png h2_Shadow_Walker_new_adult.png h4_cavelurker.png h4_cavelurker2.png h4_cavelurkers1.gif h4_cavelurkers2.png h5_gravedigger1.png h5_gravedigger2.png Halloween_tree.gif harvestegg.gif Harvestfemale.png Harvestmale.png harvestmales2.gif Harvests1.gif harvest_females2.gif Hellfireegg.gif hellfirefemales2.png hellfiremales2.png hellfires1.gif Hellfire_Wyvern_Female.gif Hellfire_Wyvern_Male.gif hellhorsefemale.png hellhorsemale.png Horse.png Horsedragonegg.gif Horse_Hatchling.gif Horse_s2.gif Iceegg.gif Ice_Adult.gif Ice_Hatchling.gif Ice_s2.gif ii_Water_female.gif ii_Water_male.gif ii_Water_s1.gif ii_Water_s2f.gif ii_Water_s2m.gif j_GON.gif j_GON_egg.gif j_GON_s1.gif j_GON_s2.gif Leetle.gif LeetlePalm.png leetletree.gif Leetle_tree.gif lumina1.png lumina2.png luminaegg.png luminas1.png luminas2.gif Magi3.gif Magiegg.gif Magi_Hatchling.gif Magi_s2.gif magmaegg.gif Magma_Adult.gif Magma_Hatchling.gif Magma_s2.gif Mint3.gif Mintegg.gif Mint_Hatchling.gif Mint_s2.gif Moonsongs1.gif moonstones2female.gif Moonstone_egg.GIF Moonstone_female_adult.png Moonstone_male_adult.png Moonstone_Male_Hatchling.gif Nebulablues2.gif Nebulagreens2male.gif nebulapurplemale.png Nebularedmale.gif Nebulas1.gif Nebula_egg.gif Nebula_Femaleblue.gif Nebula_green_male.gif Nebula_Males2purple.gif Nebula_red_female_hatchi.png Neoeggnew.png Neotropical.gif Neotropical_Hatchling.gif Neotropical_male_.gif Neo_Hatchling.gif Nocturneegg.gif nocturnes1.gif nocturnes2a.gif Nocturne_Adult.gif Nocturne_Adult_Female_Night_Form_New.png Nocturne_night_adult.png Nocturne_night_hatchie.png Nocturne_night_hatchie_1.png Ochredracke.gif ochredrakes2.gif Ochredrake_Egg.gif Ochredrake_Hatchling.gif olive1.png olive2.png Olives1.gif olives2.gif Paper.gif paperegg.gif Paper_1st_stage.gif Paper_2nd_stage_hatchling.gif pillowegg.gif Pillowfemale.png Pillowmale.png pillows1.gif pillows2.png Pillows2a.gif Pink.gif Pinkegg.gif Pinkfemale.gif Pink_female_hatchling.gif Pink_Hatchling.gif Pri01_GoldtinS1.gif Pri01_Goldtins2.gif Pri01_Goldtinsel.png Pri01_Goldtinselegg.gif Pri02_Silvertinegg.gif Pri02_Silvertins1.gif Pri02_Silvertins2.gif Pri02_Silvertinsel.png Pri03_Bronzetinegg.gif Pri03_BronzetinS1.gif Pri03_bronzetins2.gif Pri03_Bronzetinsel.png Pri04_goldshimmer.png Pri04_goldshimmers1.png Pri05_silvershimmers1.png Pri05_Silvershimmers2.png Pri06_Bronzeshimmer.png Pri06_bronzeshimmers2.png Purpleegg.gif purples2.gif Purple_female.png Purple_male.gif Purple_s1.gif PygmyEgg.gif Pygmyfemale.gif Pygmymale.gif Pygmys2male.gif Pygmy_Hatchling.gif Pygmy_Mature.gif pyg_crimsomflaes1.gif pyg_Crimsomflare.gif pyg_CrimsomFlareegg.gif pyg_crimsomflares2.gif pyg_Misfitegg.gif pyg_misfitfemale.gif pyg_Misfitmale.gif pyg_misfits1.gif pyg_misfits2.gif pyg_Nilia.gif pyg_Niliaegg.gif pyg_Nilias1.gif pyg_Nilias2.gif pyg_Seawirmegg.gif pyg_seawirmmale.gif pyg_seawirms2.gif pyg_Seawyrm_pygmy_male_adult.gif py_DarkMystegg.gif py_Darkmystfemale.gif py_DarkMystmale.gif py_darkmysts1.gif py_darkmysts2a.gif py_DarkMysts2b.gif Red3.gif Redegg.gif Red_s1.gif Red_s2.gif Ridgewingaltegg.gif Ridgewingaltfemale.gif Ridgewingalts1.gif ridgewingalts2a.gif Ridgewingalts2female.gif ridgewingegg.gif Ridgewingfemale.gif Ridgewingmale.gif Ridgewings1.gif ridgewings2.gif Ridgewings2a.gif royalblue2.png royalblueegg.png RoyalblueFemale.png royalblues1.gif royalcrimsoms1.png royalcrimson.png Seasonal_1spring1.png Seasonal_1spring2.png Seasonal_1springs1.gif Seasonal_1springs2.gif Seasonal_1summer.png Seasonal_1summer2.png Seasonal_Fall1.png seasonal_Fall2.png Seasonal_falls2.gif Seasonal_Winterm.png Seasonal_Winter_Adult_Female.png Seasonal_Winter_Egg.gif Seasonal_Winter_S1.gif Seasonal_Winter_S2_Fem.gif Seasonal_Winter_S2_Male.gif seragama1.png seragamas1.png seragamas2f.png seragamas2m.png sere_Neglect-ungen.gif sere_Neglectedegg.gif sere_Neglected_female.png sere_Neglected_Hatchling.gif sere_Neglected_male.png sere_Neglected_s2.gif Silver3f.gif Silver3m.gif Silveregg.gif Silver_Hatchling.gif Silver_male_hatchie.png Silver_Mature.gif Skywing3.gif Skywingegg.gif Skywings1.gif Skywings2.gif soulpeacef.png soulpeacem.png speck.gif speckledthroat1.png speckledthroat2.png SpeckleThroategg.gif Specklethroats1.png Spitfire.png Spitfireegg.gif spitfires1.gif spitfires2.gif Spring_tree.png Stone.gif Stone3.gif Stones2.gif Stone_Hatchling.gif stripeblackf.png stripeblackm.png stripebluef.png stripebluem.png striped_eggWhite_.png striped_White_f.png striped_White_male.png striped_White_s1.png striped_White_s2.png stripegreenf.png stripegreenm.png striperedf.png striperedm.png stripereds1.gif stripereds2.gif stu_yellowcrownf.png stu_Yellowcrownm.png stu_yellowcrowns1.gif stu_yellowcrowns2a.gif sunegg.gif Sunrisefemale.gif Sunrises2.gif Sunrise_Hatchling.gif Sunrise_male.gif Sunsetfemale.png Sunsetmale.png Sunsets2.gif Sunset_Hatchling.gif Sunsongegg.gif Sunsongs1.gif sunsongs2f.png Sunsongs2m.gif Sunsong_Amphipteres_Male.png Sunsong_Amphiptere_female.png sunstonegg.gif Sunstones1.gif Sunstones2.gif Sunstone_Adult.png swallowtailegg.gif Swallowtailfemale.png Swallowtailmale.png swallowtails1.png swallowtails2a.png swallowtails2m.png Tangaregg.gif tangars1.gif Tangars2.gif tangars3f.png tangars3m.png tb_blackcapegg.png tb_blackcapf.png tb_blackcapm.png tb_blackcaps1.gif terraeegg1.gif terraeegg2.gif terraeegg3.png Terraefemale.png Terraefemales2.gif terraemale.png Terraes1.gif Terraes2male.gif Thunder-egg-new-new.gif Thunder_Adult.gif Thunder_Hatchling.gif Thunder_s2.gif tidal_redfinned1.png tidal_redfinned2.png tidal_redfinnedegg.png tidal_redfinneds1.gif tryhornegg.png tryhornf.png tryhornm.png tryhorns1.png tryhorns2.png tsunami1.png tsunami2.png tsunamis1.gif turpentine.png turpentines1.gif turpentines2.gif ty_Nhiostrife.png ty_Nhiostrifeegg.gif Ultraviolet1.png ultraviolet2.png ultraviolets2.png Val01_Val09.gif Val01_Val09egg.gif Val01_Val09s1.gif Val01_Val09s2.gif Val02_Sweetlingegg.gif Val02_Sweetlingm.gif Val02_Sweetlingm_Alt.gif Val02_sweetlings1.gif Val02_Sweetlings1alt.gif Val02_Sweetlings2.gif Val02_Sweetlings2_Alt.gif Val03_rosebudegg.gif Val03_Rosebudf.gif Val03_rosebuds1.gif Val03_Rosebuds2.gif Val04_Heartseeker.png Val04_heartseekers1.gif Val04_heartseekers2.png Val05_asani.png Val05_asanis1.gif Val05_asanis2.gif Val06_radiantangel.png val06_radiantangels2.png Vamp3f.gif Vamp3m.gif Vampirehatch1.gif Vampirehatchling.gif Vamp_egg.gif Vamp_hatchie_male.png wateregg.gif waterhorseegg.gif WaterHorsef.gif WaterHorses1.gif Waterhorses2f.gif WaterHorse_male.gif Waterhorse_s2m.gif Waterwalker.gif Water_walker.gif Water_Walker_Hatchling.gif Water_Walker_Mature.gif Whiptail.gif Whiptails2.gif Whiptail_Egg.gif Whiptail_Hatchling.gif White3.gif Whiteegg.gif White_s1.gif White_s2.gif zzBlue_dino.gif zzBlue_dinoegg.gif zzBlue_Dino_Hatchling.gif zzBlue_Dino_Hatchling_S2.gif zzGreendinoegg.gif zzGreen_Dino.gif zzGreen_dino_S1.gif zzGreen_dino_S2.gif zzPurple_dino.gif zzPurple_dinoegg.gif zzPurple_Dino_S1.gif zzPurple_Dino_S2.gif zzRed_dino.gif zzRed_Dinoegg.gif zzRed_Dino_S1.gif zzRed_Dino_S2.gif zzYellow_dino.gif zzYellow_Dinoegg.gif zzYellow_dino_2nd_stage_hatchling.gif zzYello_dino_1st_stage.gif zzzZombie3.gif zzzZombie_Hatchling.gif zzzZombie_Hatchlings2.gif"
    #imglist = imglist.split(" ")
    imglist = []
    for img in os.listdir('./dragon/all'):
        if img != "Thumbs.db" and img != 'adults.txt':
            imglist.append(img)
    print(imglist)
    imgattrib = {}
    for dimg in imglist:
        imgdata=[]
        print(dimg)
        im1 = Image.open("./dragon/all/"+dimg)
        width, height = im1.size
        imgdata.append(width*height)
        imgdata.append(width)
        imgdata.append(height)
        imgattrib[dimg] = imgdata
        print(dimg,"Dimensions:", im1.size, "Total pixels:", width * height)
#     print(imgattrib)
    return imgattrib

def read_source_img(dimg):
    im1 = Image.open("./dragon/all/"+dimg)
    im1 = im1.convert("P")
    return im1

def img_compare(im1, im2):
    "Calculate the root-mean-square difference between two images"
    diff = ImageChops.difference(im1, im2)
    h = diff.histogram()
    sq = (value*(idx**2) for idx, value in enumerate(h))
    sum_of_squares = sum(sq)
    rms = math.sqrt(sum_of_squares/float(im1.size[0] * im1.size[1]))
    return rms

def img_resize(im1,im2):
    im1t = im1.resize((4,4), PIL.Image.ANTIALIAS)
    im2t = im2.resize((4,4), PIL.Image.ANTIALIAS)
    rms = img_compare(im1t, im2t)
    return rms

def check_dragonset(imgurl):
    thecheck={}
    #print img
    try:
        sock = urllib.request.urlopen(imgurl,data=None)
        imgSource = sock.read() 
        f = BytesIO(imgSource)
    except IOError:
        f = 'spacer.png'
    try:
        im1 = Image.open(f)
    except IOError:
        return 9999
    width, height = im1.size
    hist1 = im1.histogram()
    hist2 = []
    #print(imgurl,"Dimensions:", im1.size, "Total pixels:", width * height)
    min_rms = 9999
    min_k = 'zzzz'

    tfound = False
    for k in imgattrib:
        imgdata =[]
        imgdata =imgattrib[k]
        im2 = read_source_img(k)
        thist = False
        width2 = imgdata[1]
        height2 = imgdata[2]
        hist2 = im2.histogram()
        #rms = img_resize(im1,im2)
        if  width2 == width and height2 == height:
            tfound = True
            thist = (hist1 == hist2)
            rms = img_compare(im1, im2)
            if rms < min_rms:
                min_rms = rms
                min_k = k
            print("match",hist1 == hist2, rms)
        
    if tfound:
        imgdata =[]
        imgdata =imgattrib[min_k]
        im2 = read_source_img(min_k)
        thist = False
        width2 = imgdata[1]
        height2 = imgdata[2]
        hist2 = im2.histogram()
        print(imgurl,min_k,width,height,width*height,tfound,thist)
        print(imgurl,width,height)
        print(hist1)
        print(min_k,width2,height2)
        print(hist2)
        rms = img_compare(im1, im2)
        print("match",hist1 == hist2, rms)
        k1 = min_k
        if rms > 100:
            print("** fake find **")
    else:
        print(imgurl,"***",width,height,width*height,"Not Found")
        k1 = "spacer.png"
        rms = 99999
        
    
    print("------------")
    thecheck["im1"] = imgurl
    thecheck["w1"] = width
    thecheck["h1"] = height
    thecheck["hist1"] = hist1
    thecheck["im2"] = k
    thecheck["w2"] = width2
    thecheck["h2"] = height2
    thecheck["hist2"] = hist2
    thecheck["matchsize"] = tfound
    thecheck["matchcolor"] = thist
    thecheck["rms"] = rms
    thecheck["result"] = k1
    thecheck["found"] = True
    if k1 == "spacer.png":
        thecheck["found"] = False
    return thecheck


thescroll = get_owner()
print(thescroll)
if thescroll < " ":
    thescroll="khione"

knownbreed_dict = {}
knownbreed_dict['/images/00ef.png'] = "Wrapping Wing"

unkknownbreed_dict = get_unkbreed_dict()

imgattrib = {}
imgattrib = load_saved_imgs()

breeds = {}
f = open('breedids'+thescroll+'.xml', 'w')
f.write('<?xml version="1.0"?>\n')
f.write('<data>\n')
for k in unkknownbreed_dict:
    f.write('<breedid name="'+k+'">\n')
    f.write('   <path>'+k+'</path>\n')
    imgurl = "http://dragcave.net"+k
    theimg = check_dragonset(imgurl)
    
    f.write('   <im1>\n')
    f.write('      <imgurl>'+imgurl+'</imgurl>\n')
    f.write('      <width1>'+str(theimg["w1"])+'</width1>\n')
    f.write('      <height1>'+str(theimg["h1"])+'</height1>\n')
    histlist = ','.join(str(e) for e in theimg["hist1"])
    f.write('      <histogram1>'+histlist+'</histogram1>\n')
    f.write('   </im1>\n')
    f.write('   <im2>\n')
    f.write('      <imgurl>'+theimg["result"]+'</imgurl>\n')
    f.write('      <width2>'+str(theimg["w2"])+'</width2>\n')
    f.write('      <height2>'+str(theimg["h2"])+'</height2>\n')
    histlist = ','.join(str(e) for e in theimg["hist2"])
    f.write('      <histogram2>'+histlist+'</histogram2>\n')
    f.write('   </im2>\n')
    f.write('   <imgtoid>'+imgurl+'</imgtoid>\n')
    f.write('   <matchid>'+theimg["result"]+"</matchid>\n")
    f.write('   <found>'+str(theimg["found"])+'</found>\n')
    f.write('   <matchsize>'+str(theimg["matchsize"])+'</matchsize>\n')
    f.write('   <matchcolor>'+str(theimg["matchcolor"])+'</matchcolor>\n')
    f.write('   <rms>'+str(theimg["rms"])+'</rms>\n')
    f.write('</breedid>\n')
    breeds[k] = theimg
    
f.write('</data>\n')
f.close()
print("That's all folks")


dragons = [] 
the_dict = {}
dragons.append(the_dict)
dragons.append(the_dict)
 
dragons = read_dragons()


newbreed_dict = dragons[0]
breed_err = dragons[1]
sorted_breed_dict = sorted(newbreed_dict, key=newbreed_dict.get)
#print(breed_err)
#print(unkknownbreed_dict)
#print(sorted_breed_dict)

print("xml saved")
