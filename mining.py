from AutoComplete import *
import clr
clr.AddReference('System.Speech')
from System.Speech.Synthesis import SpeechSynthesizer

spk = SpeechSynthesizer()

def sayTTS(text):
    spk.Speak(text)

packAnimals = []

# def SetupPets():
#     if Misc.CheckSharedValue("firebeetle"):
#         localfirebeetle = Misc.ReadSharedValue("firebeetle")
#     else:
#         localfirebeetle = Target.PromptTarget('Target your fire beetle:')
#         Misc.SetSharedValue("firebeetle", localfirebeetle)
    
#     if localfirebeetle != 0:
#         global myFireBeetle
#         myFireBeetle = Mobiles.FindBySerial(localfirebeetle)

#     if Misc.CheckSharedValue("packbeetle"):
#         localpackbeetle = Misc.ReadSharedValue("packbeetle")
#     else:
#         localpackbeetle = Target.PromptTarget('Target your pack animal:')
#         Misc.SetSharedValue("packbeetle", localpackbeetle)

# def FindPackAnimals():
#     # if findtype 292 true as mob
#     #     overhead 'Found pack llama'
#     #     @setvar! packanimal mob
#     # elseif findtype 291 true as mob
#     #     overhead 'Found pack horse'
#     #     @setvar! packanimal mob
#     # elseif findtype 791 true as mob
#     #     overhead 'Found blue beetle'
#     #     @setvar! packanimal mob
#     #     @setvar! blueBeetle mob
#     #     // ridable pack animals
#     # endif
#     return

# def SmeltOre():
#     if Player.Mount.ItemID == 169:
#         ores = Items.FindAllByID(0x19B7, -1, Player.Backpack)
#         for ore in ores:
#             Items.UseItem(ore)
#             Target.WaitForTarget(500)
#             Target.TargetExecute(Player.Mount.Serial)
#             Misc.Pause(250)

# Player.HeadMessage(54, "AutoMiner - v0.1")

# def GetMount():
#     if Player.Mount != None:
#         Misc.SetSharedValue( 'mount', Player.Mount.Serial )
#         return Mobiles.FindMobile(Player.Mount.Serial)
#     elif not Misc.CheckSharedValue( 'mount' ):
#         return Mobiles.FindBySerial( Misc.ReadSharedValue( 'mount' ) )
#     else:
#         return None

# myMount = GetMount()
# if myMount != None:
#     Player.HeadMessage(54, "I am riding a %s" % myMount)
# else:
#     Player.HeadMessage(54, "I am not riding anything")

# myPackies = FindPackAnimals()
# for packie in myPackies:
#     # show the packie name overhead
#     Player.HeadMessage(54, "Found pack animal: %s" % packie.Name)

fireBeetle = None
packie = None

miningAttempts = 0
if Player.Mount:
    Mobiles.UseMobile(Player)

for pet in Player.Pets:
    if pet.ItemID == 0x00A9: # Fire Beetle
        fireBeetle = pet
        Player.HeadMessage(33, "Found your fire beetle")
    elif pet.ItemID == 0x0124: # Pack Llama
        packie = pet
        Player.HeadMessage(33, f"Found your pack llama")

def SmeltOre():
    backpackOres = Items.FindAllByID([0x19B9, 0x19B8, 0x19B7], -1, Player.Backpack.Serial, True) # Ore ID
    if not fireBeetle or not backpackOres:
        return
    
    for ore in backpackOres:
        if ore.ItemID == 0x19B7 and ore.Amount < 2:
            continue
        Items.UseItem(ore)
        Target.WaitForTarget(500)
        Target.TargetExecute(fireBeetle.Serial)
        Misc.Pause(250)

def MoveIngots():
    backpackIngots = Items.FindAllByID(0x1BF2, -1, Player.Backpack.Serial, True)
    if not packie or not backpackIngots:
        return
    
    if packie and backpackIngots:
        for ingot in backpackIngots:
            Items.Move(ingot, packie, 60000)
            Misc.Pause(250)

playerLastPostion = Player.Position
def CheckMoving():
    isMoving = playerLastPostion != Player.Position
    playerLastPostion = Player.Position
    return isMoving

Journal.Clear()
while not Player.IsGhost:
    if Gumps.CurrentGump() == 1565867016:
        sayTTS("Captcha detected")
        Misc.Pause(1000)
        continue

    if Player.Mount:
        if not Timer.Check("mount_warning"):
            Player.HeadMessage(52, "Dismount to start mining.")
            Timer.Create("mount_warning", 2000)
        Misc.Pause(250)
        continue

    shovel  = Items.FindByID(0x0F39, -1, Player.Backpack.Serial, True) 
    if not shovel and not Timer.Check("shovel_warning"):
        Player.HeadMessage(52, "You are out of shovels")
        Timer.Create("shovel_warning", 2000)
        continue

    if not Timer.Check("mining_timer"):
        Items.UseItem(shovel)
        Target.WaitForTarget(650)
        Target.Self()
        Timer.Create("mining_timer", 2000)
        miningAttempts += 1

    if Journal.SearchByType("You dig some", "System"):
        Player.HeadMessage(52, "Ore!")
        miningAttempts = 0
    elif Journal.SearchByType("You loosen some rocks", "System"):
        miningAttempts = 0
    elif miningAttempts >= 4:
        Player.HeadMessage(52, "Time to move on.")
        sayTTS("No resources to mine")
        miningAttempts = 0

    Journal.Clear()

     # smelt ores with fire beetle
    SmeltOre()
    MoveIngots()
