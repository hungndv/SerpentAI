# SerpentAI

conda activate serpent
serpent launch d2
serpent play d2 Serpentd2GameAgent
serpent visual_debugger


serpent capture frame d2 1
serpent capture context d2 1 main_menu
serpent capture region d2 1 MAIN_MENU_OPTIONS

serpent train context 8
pip install --force-reinstall tensorflow==1.5.1

spritex datasets/collect_frames_for_context/main_menu/frame_1530767434.1339352.png

serpent capture region d2 1 BUTTON_SINGLE_PLAYER
import serpent.cv
serpent.cv.isolate_sprite("datasets/collect_frames/BUTTON_NORMAL", "SPRITE_BUTTON_NORMAL_0.png")

subprocess.call("D:/Softwares/Diablo 2/PlugY.exe -w", stdout=FNULL, stderr=FNULL, shell=False)