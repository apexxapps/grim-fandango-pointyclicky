# The outline review (15 Nov 2026)

Every object view the tools couldn't outline (build/outlines/review.json,
from `tools/outlines.py` then `tools/hotspots.py`: 112 views), decided from the
contact sheets (`tools/sheets.py`): **drawn** by hand into data/hotspots (checked
like a traced outline: it holds the game's point, isn't a sliver, isn't far
bigger than the thing's reach), **live** (a character, found where it's drawn),
**covered** (we already have it under mouse.lua's name for it), or **left**
with the reason. Hand-drawn outlines stay through a re-run of hotspots.py
(it keeps an outline of ours that holds the game's point).

Totals: 64 left, 30 drawn, 17 live, 1 covered.

| Set | Angle | Object | Outcome | Why |
|---|---|---|---|---|
| al | 0 al_allls | big door (`ga_door`, altx014) | left | never offered as an object: made untouchable at creation (al.lua line 335), nothing makes it touchable; the doorway is already the cyan 'gate' walk path (altxa00, target = ga_door's position) and the door itself is outlined as ga_door_obj (altxa01) |
| al | 0 al_allls | big door (`ga_door_obj`, altx014) | covered | already outlined under mouse.lua's rename to `/altxa01/big door` |
| al | 0 al_allls | door (`st_door`, altx012) | left | the street door is behind/at the camera (y=0.86, point projects onto the left wall's window at y=26); the exit is already the cyan 'street' walk path along the bottom edge |
| at | 2 at_intbw | catwalk (`ledge`, attx006) | left | no catwalk at the game's point: the object is created at the set origin (0,0,0, same as Bone Wagon, at.lua:634) so (374,379) lands on the floor by the wagon; the catwalk is used through the bone-wagon button handler (at_bw_handler, at.lua ~443-451: LOOK/USE keys call at.ledge.lookAt/use) once Manny is in the wagon, not by pointing |
| at | 2 at_intbw | sewer (`zw_door`, attx014) | left | never offered: made untouchable at creation (at.lua:846) and never made touchable anywhere; the sewer exit is reached by walking, not pointing |
| bi | 1 bi_kitdr | beatniks (`patrons2`, bitx417) | left | no beatnik drawn at the point on this angle: it lands on an empty chair and table seen through the club doorway, inside the cyan exit to the club; patrons2 is also made untouchable in year four (bi.lua line 844) |
| ce | 0 ce_estla | door (`cl_door`, cetx003) | left | the exit is already a walk path here: cyan 'overthere' region (604-632 x 169-399) covers the point at the right edge |
| ce | 0 ce_estla | door (`ev_door`, cetx002) | left | the exit is already a walk path here: cyan 'down' region covers the archway under the stairs, point inside |
| ce | 2 ce_front | door (`cc_door`, cetx001) | left | the exit is already a walk path here: cyan 'in' region (173-249 x 212-296) covers the cafe doorway, point inside |
| ci | 0 ci_stpws | door (`cc_door`, citx066) | left | never offered: made untouchable at creation (ci.lua:639), never made touchable; the upstairs doorway is already the cyan 'up3' walk path, which contains (278,172) |
| ci | 2 ci_widha | Glottis (`glottis_obj`, citx045) | live | a character: found where `glottis` is drawn (characters' live outlines); the fixed outline is only the fallback |
| ci | 3 ci_glotk | door (`cc_door`, citx066) | left | never offered: made untouchable at creation (ci.lua:639), never made touchable in any script |
| ci | 3 ci_glotk | Glottis (`glottis_obj`, citx045) | live | a character: found where `glottis` is drawn (characters' live outlines); the fixed outline is only the fallback |
| ci | 3 ci_glotk | bottle of gold flake liqueur (`liqueur`, citx047) | drawn | the counter-top bottles just left of the coffee urn at the foot of the bar cabinet, around the game's point (stops short of the urn's body) |
| cl | 0 cl_rubws | door (`ce_door`, cltx001) | drawn | no door is drawn: it is behind/below the camera and the exit fires when Manny walks into the ce_box trigger sector at the bottom edge (projects to y 446-480, x 106-640). Polygon covers the grated walkway from the game's point down to that strip, so the only exit off the roof can be pointed at (this angle has no walk path) |
| cn | 2 cn_rulws | door (`ci_door`, cntx249) | drawn | the open doorway in the arch behind the round vault door, incl. the disc's top where the game's point sits; the cyan 'back' walk region overlaps it but walks to (-0.25,0.87), 0.65 m from the door's use point, not into ci_box |
| co | 0 co_winws | window (`le_door`, cotx015) | drawn | the window glass behind the desk (exit to the ledge), cut above the memos; NB papers2 (cotx023) polygon already wraps the whole back wall incl. this window |
| co | 0 co_winws | papers (`papers`, cotx017) | left | the point (360,246) sits on the paper pile under memo2's outline (cotx032 covers 353-394 x 221-265); no free pixels for it without swallowing the memo; the same papers handlers are offered via papers2 cotx023 and papers3 cotx024, whose .parent is co.papers (co.lua 375/383) |
| dd | 0 dd_estws | dock workers (`barrel_bees`, ddtx046) | left | the dock workers are tiny live actors at the far pier end on this wide shot; the pier end is the cyan 'workers' walk path (point inside), which takes Manny to dd_barla where the dock workers have their outline (ddtx046) |
| dd | 0 dd_estws | dry docks (`dry_docks`, ddtx058) | left | point lands on the dark hillside above the pier end; the dry dock isn't visibly drawn on this angle; it is only touchable in year four (dd.lua line 174) and the set enters on dd_barla, where it is outlined (setup 1) |
| dd | 0 dd_estws | bridge (`hb_door`, ddtx071) | left | touchable FALSE at creation (dd.lua line 539), walked through via hb_box; the exit is the cyan 'circle' walk path at the bottom (target 7.39,-2.69 = hb_door's position) |
| dd | 0 dd_estws | door (`lx_door`, ddtx150) | left | touchable FALSE at creation (dd.lua line 557), never made touchable; walked through via lx_box; point sits inside the cyan 'workers' walk path here and dd_barla has the cyan 'lighthouse' walk path |
| dd | 0 dd_estws | tools (`tools`, ddtx063) | left | the tools only exist during the strike as an object-state bitmap (dd_0_tools.bm, dd.lua line 189) the sheet doesn't show; the point lands on bare pier, so there's no visible shape to trace. Needs a sheet rendered with the strike state (flavour only: lookAt/pickUp are just lines) |
| dd | 1 dd_barla | dock workers (`barrel_bees`, ddtx046) | left | already covered by our ddtx046 hotspot (pentagon 245-383 x 280-425 round the bee at the barrel); the game's point sits in open air between the bees, and the script moves it at runtime (dd.lua lines 211-219) |
| dd | 1 dd_barla | dry docks (`dry_docks`, ddtx058) | drawn | the dry dock's wooden ship ribs and hull frame above the far skyline, left of the foreground pillar; point sits at its lower edge. Overlaps the small 'workers' outline (same id ddtx058), but they're never touchable together (year four only vs before) |
| dd | 1 dd_barla | bridge (`hb_door`, ddtx071) | left | touchable FALSE at creation (dd.lua line 539); the exit is already a walk path here: cyan 'back' region (14-79 x 216-401) covers the point |
| dd | 1 dd_barla | striking bees (`striking_bees`, ddtx068) | drawn | APPROXIMATE: the strikers are live actors (not in the background) standing round the barrel during the strike; box round the game's point, sized from the neighbouring bee outline. Overlaps dock workers/terry outlines only in space: those are untouchable during the strike (dd.lua lines 181-185) |
| fo | 0 fo_berws | door (`fh_door`, fotx189) | left | the exit is already a walk path here: cyan 'door' region (487-604 x 113-325) covers the round doorway, point inside; its lookAt is only the default 'way out' line |
| ga | 5 ga_rckws | Glottis' eyes (`glottis_eyes`, gatx116) | left | never offered: no handlers, made untouchable at creation (ga.lua line 461) and again at lines 82 and 335, never touchable |
| ga | 7 ga_ofcha | Glottis' eyes (`glottis_eyes`, gatx116) | left | never offered: no handlers, made untouchable at creation (ga.lua line 461) and again at lines 82 and 335, never touchable |
| gt | 0 gt_estws | door (`bb_door`, gttx002) | left | the exit is the walkway's edge at the bottom-left; the cyan 'left' walk path covers it (point 2 px outside) and walks to (0.03,-1.49), 0.35 m from bb_door's out point; range 0, a walk-box door (bb_box) |
| gt | 0 gt_estws | door (`sl_door`, gttx004) | left | 3D point is up at the top of the stairs (z 22.2) and projects onto the tower's central pillar, not the stairs; the tower is the cyan 'tower' walk path here and the stairs are the 'up' walk path on setup 1 (gt_extst) |
| gt | 0 gt_estws | door (`tb_door`, gttx003) | drawn | the right archway at the tower's foot, from the arch's lower half to the floor where the game's point sits (tb_door, range 0, walk-box exit); inside the cyan 'tower' region |
| ha | 2 ha_intls | Eva (`eva_obj`, hatx143) | live | a character: found where `eva` is drawn (characters' live outlines); the fixed outline is only the fallback |
| hl | 0 hl_dorrv | door (`mx_door`, hltx183) | left | made untouchable when it is created and never made touchable again (hl.lua line 987); it is a walk-in exit, already covered by the cyan 'maxoff' walk path around the doorway (97-145 x 237-327), which contains the point |
| hl | 1 hl_elews | Glottis (`glottis_obj`, hltx139) | live | a character: found where `glottis` is drawn (characters' live outlines); the fixed outline is only the fallback |
| hl | 1 hl_elews | door (`hh_door`, hltx184) | left | the elevator door is already covered by the cyan 'outdoor' walk path (46-86 x 255-395), which contains the point (58,339) and leads to the door's use point; walkOut only |
| hl | 1 hl_elews | door (`hk_door`, hltx182) | left | the kitchen doorway is already covered by the cyan 'kitchen' walk path (235-355 x 197-396), which contains the point (298,325); walkOut only |
| hq | 2 hq_elews | elevator (`al_door`, hqtx152) | drawn | the upper part of the grey elevator door at the back (the whole visible door, 237-342 x 145-223, is over max_area, so the central 76x74 px) |
| jb | 0 jb_garin | Bone Wagon (`bone_wagon`, jbtx025) | left | already covered by our Bone Wagon hotspot (jbtx025) on this angle; the game's point (376,145) is in empty air about 20 px above the wagon's outline, on the back wall |
| le | 0 le_alloh | hanging rope (`rope_down`, letx001) | drawn | where the hanging rope goes over the ledge edge, just below it; the rope is a costume actor (tie_rope, le.lua:202-208), not in the background, so the strip follows the game's point rather than a drawn rope; the carried strip at x 292-312 misses the point by ~13 px |
| le | 2 le_ladws | hanging rope (`rope_down`, letx001) | drawn | the rope's spot on the red wall just under the ledge, left of the gargoyle (rope is the tie_rope costume, not in the background); stops left of the grappling hook / loose end points |
| lx | 0 lx_dokla | door (`li_door`, lxtx007) | left | untouchable at creation (lx.lua line 177), never made touchable; its walkOut just calls lighthouse_door, which is outlined here (lxtx008) and has the cyan 'lighthouse' walk path |
| lx | 0 lx_dokla | door (`top`, lxtx010) | left | a 3 px doorway at the lantern on this wide shot, inside the lighthouse door's outline and 'lighthouse' walk path; it's the exit for when Manny is up top (z=3.03), so it belongs on the close angles, not here |
| lx | 1 lx_extoh | door (`li_door`, lxtx007) | left | untouchable at creation (lx.lua line 177); the same door is outlined here as lighthouse_door (lxtx008, 295-328 x 244-302) |
| ly | 1 ly_intha | Chowchilla Charlie (`charlie_obj`, lytx103) | live | a character: found where `charlie` is drawn (characters' live outlines); the fixed outline is only the fallback |
| ly | 1 ly_intha | Meche (`meche_obj`, lytx108) | live | a character: found where `meche` is drawn (characters' live outlines); the fixed outline is only the fallback |
| me | 0 me_carla | door (`door`, metx060) | drawn | the greenhouse door: lower-left corner of the greenhouse on the hilltop (inside the cyan 'greenhouse' walk path) |
| me | 0 me_carla | greenhouse (`greenhouse`, metx057) | drawn | greenhouse on the hilltop: dome and left block, leaving out the door at its lower-left corner (inside the cyan 'greenhouse' walk path) |
| me | 1 me_pmpws | greenhouse (`greenhouse`, metx057) | drawn | greenhouse on the hill: tower top, dome and left wall, notched around our existing door hotspot (360-366 x 185-213); the right wall section is left out to keep it under 10 vertices |
| me | 2 me_shtgh | greenhouse (`greenhouse`, metx057) | drawn | the whole greenhouse: glass tower, left block and dome, from x=72 (right of our door hotspot at the left edge) to the right end of the dome |
| me | 5 me_rerha | greenhouse (`greenhouse`, metx057) | drawn | overhead: glass tower and dome body, tracing around our door hotspot (294-390 x 93-168) and keeping right of the Salvador's head/car hotspots at the top left. 12 vertices, needed to go around the door |
| mg | 0 mg_morws | Coroner (`membrillo_obj`, mgtx063) | live | a character: found where `membrillo` is drawn (characters' live outlines); the fixed outline is only the fallback |
| mg | 1 mg_tblms | Coroner (`membrillo_obj`, mgtx063) | live | a character: found where `membrillo` is drawn (characters' live outlines); the fixed outline is only the fallback |
| mo | 0 mo_ddtws | tube (`tube`, motx083) | left | nothing drawn at the point on this angle: (190,372) is bare floor (the floor square is the tile pattern); the tube is on the desk and outlined on setup 1 (motx083); the carried Grim Mouse floor polygon for motx083 is 12 px below the point |
| mo | 1 mo_winws | Meche (`meche_obj`, motx122) | live | a character: found where `meche` is drawn (characters' live outlines); the fixed outline is only the fallback |
| mt | 0 mt_diaha | fountain (`fountain`, mttx032) | drawn | the whole fountain basin (rim to front step); touchable once Chepito leaves (mt.lua:20), when Chepito's own outline at the same spot goes |
| mt | 1 mt_diats | fountain (`fountain`, mttx032) | drawn | the whole fountain basin in the foreground, rim to base; touchable once Chepito leaves (mt.lua:20) |
| mt | 3 mt_gltrv | doorway (`tg_door`, mttx030) | left | the point visibly sits off the thing: (107,238) is on the dark track bed under the mural, ~100 px left of the sky-lit opening to the temple gate (about 205-242 x 138-225); nothing at the point to outline. This is the only angle where the doorway projects on screen and there's no cyan walk path to it, so as it stands the exit is unreachable by pointing: needs a decision |
| mx | 2 mx_maxcu | Maximino (`max_obj`, mxtx068) | live | a character: found where `maximino` is drawn (characters' live outlines); the fixed outline is only the fallback |
| my | 1 my_glofg | outside (`bs_door`, mytx048) | drawn | 'outside': the big opening at the top right, the same extent as the cyan 'out' walk path. Drawn as an object so its lookAt (not just walkOut) can be reached |
| my | 1 my_glofg | mechanic (`mechanic2`, mytx024) | left | already covered by our hotspot under the renamed id mytx024_1 (285-324 x 140-195), which contains the point (307,160); the mytx024 hotspot is the other mechanic, at 390-419 |
| nl | 1 nl_legla | sign (`sign`, nltx020) | drawn | a patch of the neon lady's red dress around the point (the sign is far bigger than max_area; clear of the arm outline) |
| nl | 1 nl_legla | window (`window1`, nltx017) | drawn | the lit window in the building below the lady's foot (touchable until the lady drops, nl.lua 56) |
| nl | 2 nl_neoha | sign (`sign`, nltx020) | drawn | a patch of the sign's scaffolded back panel around the point, left of the lady's leg and right of the ladder |
| pc | 1 pc_dorws | bridge (`bp_door`, pctx002) | left | the exit is already a walk path: cyan 'bridge' covers the archway (point 12 px left, on the lamp post) and walks to (0.41,1.45), 0.27 m from bp_door |
| pc | 1 pc_dorws | door (`pi_door`, pctx001) | left | the exit is already a walk path: cyan 'station' covers the doorway and its target (-0.06,5.57) is the door's own position |
| ps | 0 ps_widha | Chepito (`chepito_obj`, pstx022) | live | a character: found where `chepito` is drawn (characters' live outlines); the fixed outline is only the fallback |
| ps | 0 ps_widha | Glottis (`glottis_obj`, pstx017) | live | a character: found where `glottis` is drawn (characters' live outlines); the fixed outline is only the fallback |
| ps | 0 ps_widha | lantern (`lantern`, pstx029) | left | Chepito carries the lantern: every frame ps.chepito_light moves its interest actor to Chepito's node 12 (ps.lua line 30), so the fixed point (160,288) on the sub hull is stale. Nothing is there; the lantern is on Chepito, who has the magenta actor hotspot. Needs an actor-following hotspot if lantern look/use should be separate from Chepito |
| ps | 0 ps_widha | octopus (`octopus`, pstx007) | left | already covered by our octopus hotspot (pstx007) on this angle; the point (120,160) is in empty dark water about 10 px left of it, with no octopus shape visible |
| ps | 1 ps_barfg | octopus (`octopus`, pstx007) | left | point (195,81) is in empty dark water above the sub, with no octopus visible at it (the nearest shape is the large creature silhouette about 80 px right, at the top). Reachable on setup 0 via the pstx007 hotspot; lookAt/use there only give lines |
| re | 0 re_estla | Velasco (`velasco_obj`, retx063) | live | a character: found where `velasco` is drawn (characters' live outlines); the fixed outline is only the fallback |
| re | 1 re_front | door (`ri_door`, retx078) | left | untouchable at creation (re.lua line 525), never made touchable; the doorway is the cyan 'in' walk path (142-292 x 158-271), point inside |
| rf | 1 rf_rufha | x (`escape_point_1`, rftx055) | left | no handlers; holds a window object state and is set untouchable in set_up_actors (rf.lua:15); a marker for the pigeon chase, not a thing to point at |
| rf | 1 rf_rufha | x (`escape_point_2`, rftx056) | left | no handlers; holds a window object state and is set untouchable in set_up_actors (rf.lua:16); a marker for the pigeon chase, not a thing to point at |
| rf | 1 rf_rufha | ladder (`ladder_object`, rftx002) | left | the exit is already a walk path here: the cyan 'back' region (401-522 x 165-198) contains (484,176) |
| rf | 1 rf_rufha | pigeons (`pigeons2`, rftx051) | left | already covered by our pigeons hotspot rftx021 (rf.pigeons1) on this angle, which contains (138,272); pigeons2 has no handlers and is a child of it (parent = rf.pigeons1, rf.lua:1079) |
| rf | 1 rf_rufha | pigeons (`pigeons3`, rftx051) | left | already covered by our pigeons hotspot rftx021 (rf.pigeons1) on this angle, which contains (138,272); pigeons3 has no handlers and is a child of it (parent = rf.pigeons1, rf.lua:1087) |
| rf | 1 rf_rufha | sky (`sky`, rftx053) | left | never offered: made untouchable at creation (rf.lua:1095), touchable only inside the pigeon cut-scene (make_touchable rf.lua:198, untouchable again 206 before END_CUT_SCENE); its handlers are empty |
| rf | 2 rf_rufws | pigeons (`pigeons2`, rftx051) | left | already covered by our pigeons hotspot rftx021 (rf.pigeons1) on this angle, which contains (426,206); pigeons2 has no handlers and is a child of it (parent = rf.pigeons1) |
| rf | 2 rf_rufws | pigeons (`pigeons3`, rftx051) | left | already covered by our pigeons hotspot rftx021 (rf.pigeons1) on this angle, which contains (426,206); pigeons3 has no handlers and is a child of it (parent = rf.pigeons1) |
| rf | 2 rf_rufws | sky (`sky`, rftx053) | left | point at the top edge (344,12) and never offered: made untouchable at creation (rf.lua:1095), touchable only inside the pigeon cut-scene (rf.lua:198-206); handlers empty |
| sg | 1 sg_sgnha | bumpy road (`mod_door`, sgtx075) | left | the exit is already a walk path here: the cyan 'path_bd' region (394-529 x 9-128) covers the bumpy road and contains (458,101) |
| si | 0 si_ladms | booze (`booze`, sitx162) | left | already covered by our sitx162 hotspot (bottle 339-361 x 212-256); the game's point is 4 px right of the bottle's shoulder, within the 6 px allowance |
| si | 0 si_ladms | stuff (`scrimshaw_apparatus`, sitx183) | drawn | the tattoo apparatus: dark stand plus the knobbed arm left of the chair; only touchable while Toto is on the phone (si.lua line 807) |
| si | 1 si_frgms | Sailor (`naranja_obj`, sitx176) | live | a character: found where `naranja` is drawn (characters' live outlines); the fixed outline is only the fallback |
| si | 1 si_frgms | Toto (`toto_obj`, sitx114) | live | a character: found where `toto` is drawn (characters' live outlines); the fixed outline is only the fallback |
| sl | 0 sl_intha | they (`they1`, sltx250) | left | never offered: no handlers and made untouchable at creation (sl.lua line 821) |
| sl | 1 sl_diams | Carla (`carla_obj`, sltx222) | live | a character: found where `carla` is drawn (characters' live outlines); the fixed outline is only the fallback |
| sp | 0 sp_webws | bone (`bone_in_web`, sptx017) | left | never offered: no handlers, made untouchable at creation and on every enter (sp.lua 593, 417), never made touchable; the web (green) covers the spot |
| sp | 0 sp_webws | heart (`heart`, sptx009) | left | never offered: no handlers, made untouchable at creation and on every enter (sp.lua 522, 416), never made touchable (sp.lua 353 touches sg.heart, another set) |
| sp | 1 sp_entla | bone (`bone_in_web`, sptx017) | left | never offered: no handlers, made untouchable at creation and on every enter (sp.lua 593, 417), never made touchable |
| sp | 1 sp_entla | heart (`heart`, sptx009) | left | never offered: no handlers, made untouchable at creation and on every enter (sp.lua 522, 416), never made touchable |
| tb | 0 tb_strws | door (`hh_door`, tbtx057) | left | the exit is already a walk path: cyan 'lounge' archway walks to (-0.70,1.50), 0.12 m from hh_door's out point; the game's point projects onto the betting window (tbtx032), not a doorway |
| tg | 0 tg_gtkws | stairs (`bs_door`, tgtx044) | drawn | the stairs go down off the left end of the platform. The game's point (31,312) is in the sky over that drop, and the bs_box trigger projects to the ledge top at 67-123 x 367-369. Polygon spans the gap from the point down to the ledge, left of the tower wall and the sign |
| tg | 0 tg_gtkws | doorway (`waiting_door`, tgtx026) | drawn | the dark stone doorway left of the railroad sign's post (frame and opening, 155-193 x 302-365) |
| tg | 1 tg_trkla | stairs (`bs_door`, tgtx044) | left | point at the top edge, in the sky (261,3); the stairs trigger bs_box projects to 207-295 x 138-162, inside the cyan 'down' walk path, which already takes the player there |
| tg | 2 tg_cofws | stairs (`bs_door`, tgtx044) | drawn | as on setup 0: the stairs drop off the left end of the platform. The point (250,128) is in the sky over it, and bs_box projects to the low ledge at 240-297 x 184-190. Polygon spans the point down to that ledge, left of the tower |
| tg | 2 tg_cofws | sign (`sign`, tgtx033) | left | point (60,167) is in the empty sky; no sign is drawn on this angle's background (the sign stands by the doorway, out of this shot). Reachable on setup 0 via the sign hotspot tgtx033 |
| tg | 2 tg_cofws | doorway (`waiting_door`, tgtx026) | drawn | the dark recess on the tower's left face (354-376 x 131-192). The waiting door's column projects to x=354, y 108-189. It overlaps the over-wide Gate Keeper (top half) and mt_door doorway tgtx042 (bottom) hotspots, but contains neither of their points |
| th | 0 th_rftha | burners (`coffee_rack`, thtx091) | drawn | the hot plate with its two burners; same shape as our existing thtx091 polygon but with the top edge raised 2-5 px, so it contains the game's point (301,339), which sat on the old edge |
| th | 2 th_stgws | dressing room (`dressing_room`, thtx093) | drawn | the lit dressing-room doorway seen below through the railing, from the rail at the game's point down to the lamp-lit floor; clear of the Thunder Boy outline to the left |
| tr | 1 tr_estha | tree (`tree`, trtx049) | left | point lands on bare floor about 55 px below the hanging roots, off the tree itself on this overhead angle; the tree is outlined on setup 2 (tr_pmpws, trtx049), where Manny works the pump |
| tu | 0 tu_dorcu | deadbolt (`closed_bolt`, tutx062) | left | this background shows the cage door open (open bolt/wheel tutx067/tutx070 drawn at right); closed_bolt is live only while the door is closed (tu.lua 99/79/91), and that door is an object-state image not on this sheet, so (128,289) is empty doorway; outlined as tutx062 on setups 2 and 3 |
| tu | 0 tu_dorcu | door (`lo_door`, tutx092) | drawn | the double door at the back (to the lobby); NB the cyan 'out' path stops at y 0.44, 1.3 m short of the door, and fire extinguisher bdtx018's rectangle covers the whole back wall |
| tu | 0 tu_dorcu | red tube (`red_tube`, tutx075) | drawn | the red-banded canister tube behind the cage bars, right of the repairman, above the door wheel outline (touchable on this angle, tu.lua 541) |
| tu | 2 tu_swiha | repairman (`brennis_obj`, tutx073) | live | a character: found where `brennis` is drawn (characters' live outlines); the fixed outline is only the fallback |
| tu | 2 tu_swiha | wheel (`open_wheel`, tutx070) | left | background shows the door closed (tutx058 door wheel outlined over it); open_wheel is touchable only while it's open (tu.lua 81/93/101), drawn by an object state not on this sheet; outlined as tutx070 on setup 0 |
| tu | 3 tu_tubws | dead bolt (`open_bolt`, tutx067) | left | point lands on bare brick wall where the door would swing when open; the open door is an object state not on this background; touchable only while open (tu.lua 80/92/100); outlined as tutx067 on setup 0 |
| tu | 3 tu_tubws | wheel (`open_wheel`, tutx070) | left | point lands on the closed door's edge (tutx058); the open door is an object state not on this background; touchable only while open (tu.lua 81/93/101); outlined as tutx070 on setup 0 |
| vo | 1 vo_intha | suit of armor (`suit`, votx034) | left | not on screen on this angle: the suit stands to the right of the room on vo_amrms; (96,99) lands on the brick wall above the vault doorway (inside the metal tab's outline); reachable on vo_amrms, where our votx034 hotspot covers it |

## Found along the way (not fixed here)

- **Outlines of ours that look wrong:** co setup 0 `papers2` (cotx023) wraps
  the whole back wall, window included. tu setups 0 and 3 `extinguisher`
  (bdtx018) is a rectangle over the back wall that swallows the lobby door.
  mo setup 0 `tube` sits on bare floor. vo setup 1 `metal tab` (votx016)
  covers much of the brick wall. th "dressing room" (thtx093) is an exit
  polygon over most of the backstage floor, so a click on the floor may walk
  Manny out. rf setup 2 has strips for the two escape points, which have no
  handlers and are untouchable.
- **th's setup numbers:** th.lua has th_stgws = 0 and th_rftha = 2. The
  tools' file names say the opposite (consistent with each other); check
  which one the engine's setup index matches.
- **Possibly unreachable:** mt setup 3, the doorway to the temple gate
  (mttx030). Its point sits on the track bed, about 100 px from the opening,
  and no walk path leads there. at setup 2's catwalk is placed at the origin
  and is used through the Bone Wagon keys (docs/moments.md, line 5).
  lx.top is only a place Manny comes out at (range 0, no handlers): going
  down from the lighthouse top needs checking in the playthrough.
- **ps lantern:** Chepito carries it (ps.lua line 30 moves its point to him
  every frame), so it needs to follow his actor, as the characters do.
- **The tool:** objects whose background is swapped in by a script (tu's
  bolts and wheels: open/closed door states) fail on every angle that shows
  the other state. And a walkOut-only door whose point is inside a walk path
  could be counted as covered rather than flagged.
