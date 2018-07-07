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

serpent capture region d2 1 TEXT_LUT_GHOLEIN
import serpent.cv
serpent.cv.isolate_sprite("datasets/collect_frames/TEXT_LUT_GHOLEIN_1", "plugins/Serpentd2GamePlugin/files/data/sprites/SPRITE_TEXT_LUT_GHOLEIN_1.png")