# The moments the game takes the controls: proposals for Simon

*For Simon to approve, line by line (15 Nov 2026). Built: all 24 (vehicles 1-5; 6-24 the same day). Saves to try each: build/for-simon/README.md.*

**What counts as a moment.** A scene whose script installs its own key handler
(`system.buttonHandler = ...` in the game's scripts) instead of the normal
walk-and-act one, plus the climbs, which the game runs from its normal
handler (`is_climbing`). The generic handlers aren't moments: dialogue (39
scripts, already pointer-driven), the coat (done), the menus, and the
portholes (dp, op, ul only save and restore the handler). That leaves 24
moments (lines 1-24); lines 25-26 note two things that look like moments
and aren't. The plan's "29" counted the scripts that install a handler, and
one moment can span several (the Bone Wagon's handler is installed in five
sets).

**The rules every line follows** (PLAN.md, the laws):
- Tap = the main action, two-finger tap = look (E), the tray's Skip = Esc.
  A tap on Manny is the coat (I), or with something in hand uses it on its own
  (the 1998 U with nothing targeted; Simon, 15 Nov 2026); a swipe up while
  holding puts it away (P). Inside a moment, the moment's own rule for a tap
  on Manny (below) comes first.
- Every gesture sends the original's own keys to the scene's own handler,
  nothing else. "Held until there" means the engine holds the key the 1998
  player held (an arrow, say) and lets go when Manny, the vehicle or the
  cursor reaches the point tapped, or when the scene's own script stops it.
- No menus, no on-screen buttons: you point at the thing in the scene.
- Where Grim Mouse did it differently (screen regions calling scripts
  directly, objects it invented), the line says so. Those calls go away when
  the line is built.

Keys: ↑ ↓ ← → are the arrows (MOVE_FORWARD/BACKWARD, TURN_LEFT/RIGHT), U use,
P pick up, E examine, I inventory, Esc override.

## Vehicles

1. **Bone Wagon** (sg signpost fork, tr tree pump room, bv beaver room, lb
   lobby, bd beaver dam: `bone_wagon_button_handler`). 1998: ↑ gas, ↓
   reverse, ← → steer, U or P get out. Proposed: tap the ground = ↑ held, with
   ← or → held while the wagon isn't facing the point, until it gets there;
   tap the ground behind the wagon = ↓ held; tap the wagon = U (get out).
   Grim Mouse: invented "Bone Wagon" objects (`sg.bone_drive`,
   `na.bone_drive`) and a `driveto` script.
   **Built for Simon to try (15 Nov 2026), engine only** (HotspotMan::driveEvent
   and driveUpdate). While `bone_wagon_button_handler` is installed, every tap
   goes to the drive and nowhere else, so Grim Mouse's `driveto` is never
   reached. The way there is the game's own route through the sectors the
   wagon may use (Actor::findPath, split out of walkTo). The engine holds
   ↑ (↓ for a point behind the wagon and within 5 units) and the arrow that turns
   it, by the rule of the game's own `bonewagon.monitor_turns`, until the nose
   (or tail) is within 1.2 units of the point. It lets go when it's blocked
   (1.2 s without moving or turning), after 25 s, in a cut scene, or when the
   scene changes. A new tap re-targets. A tap on or near a way out (the set's hot
   sectors, which the game's Doorman watches) drives into it, so the game itself
   changes the scene or refuses: Glottis's "low-riding street rod" line. A tap on
   the wagon as drawn = U, two fingers = E. Proven on the bench from the save
   below: turn on the spot, drive round the trees, back up, re-target, get out
   and back in, the tree pump's way out, the bumpy road refused
   (build/bench/e1-*, d3-*, f3-*, g1-*, g3-*). The save: from a new game the
   game's own developer jump `stump` (the cut scene that takes Manny from El
   Marrow into the forest), then played by pointer: the heart ripped out, the
   bone, the scythe on the web, the heart back in Glottis, the Copal movie, the
   first ride (build/for-simon/grim13.gsv).
   **Simon tried it (15 Nov 2026): "It's not a driving experience, the point and
   click just works."** His one critique: turning is very slow.
   **The 1998 values back (15 Nov 2026).** Grim Mouse's sg.lua started the wagon
   at walk_rate 3.5 and turn_rate 40 and set its walk rate to 4 on getting in;
   the edition's sg.lua is the 1998 one there (0.5, `min_turn_rate`, nothing).
   It changes no turning: the game's own `bonewagon.monitor_turns` sets the turn
   rate every frame, in both, to **20 x the wagon's speed (world units a second),
   at most 60 degrees a second** (reached at 3 a second; top speed 4.5), and
   standing still an arrow turns it on the spot at **30 degrees a second**. The
   drive lets go of the gas while the wagon is more than 70 degrees off the way,
   so a big turn is made at 30 degrees a second or less (a U-turn: about 6 s).
   That is the 1998 rate; no faster one is invented. (A faster feel within the
   rules would be the drive's choice of keys: keeping the gas held through a
   turn gives 60 a second, on a wide circle, about 4 units across. Simon's call.)
   **Grim Mouse's `sg.bone_drive` and `na.bone_drive` are retired:** mouse.lua
   links the game's own `bone_wagon` object (sg, na, tr, lb, bv, bd; Glottis in
   at) to the wagon's actor, so a tap on the parked wagon gets Manny in wherever
   it is (the game itself moves the object's use point when he gets out); the
   sg.lua and na.lua patches no longer touch bone_drive. Saves made with them
   keep theirs, with no outline. Proven: out in sg, back in by a tap on the
   wagon, drive into na and about it, back to sg, into tr (Manny gets out, as
   the game has him), back in, and the game drives out (build/bench/w0..w13).
   **Every scene:** the handler is the same in all six sets, so the drive is.
   Proven in sg, na and tr; lb, bv and bd come later in Year 1 and weren't
   reached on the bench.
2. **Forklift** (de dillopede elevator, wc wine cellar:
   `forklift_button_handler`). 1998: ↑ forward, ↓ back (out of the shaft when
   stuck), ← → turn, U or P dismount.
   **Built (15 Nov 2026):** as the Bone Wagon, at the forklift's own scale
   (0.4 units a second, 30 degrees a second). Its arrows are simpler: Left
   always turns it left. A tap on the forklift = U; stuck in the shaft, any tap
   = ↓ (back out). Grim Mouse's invented `de.forkdrive` and `wc.forkdrive` are
   gone (and the wc.lua patch with them: wc.lua is the 1998 one): the game's own
   `wc.forklift` / `de.forklift` are linked to the forklift and stay live
   wherever it's drawn, because `de.forklift_actor.monitor_objects` flips the
   forklift's and the lever's touchable flags by which is nearer Manny (the
   keyboard's hot object). Found on the way: Grim Mouse's `Set.update_hotspots`
   loop is now guarded (an object with no range or hotspot stopped it). Proven
   (build/for-simon/grim14.gsv): get on by a tap, drive into the elevator (a way
   out), about the elevator, back out into the cellar, a tap on the forklift
   (build/bench/f4-on, f5-*, f6-b, f7-b, f8-back, f9-*).
3. **The ship's engine** (ei engine room: `engineButtonHandler`). 1998: ↑
   ahead, ↓ reverse, ← port, → starboard (each press runs one `drive_ship`),
   U, P or I let go of the controls.
   **Built (15 Nov 2026), keeping its levers:** each tap is one press, by where
   the game's own lever objects are drawn. Manny stands over the console, so the
   taps are on his hands: the left lever = → (the script's "starboard" raises
   the left lever, `mn_levers_left_up`), the right lever = ← ("port",
   `mn_levers_right_up`): the proposal had these the other way round; the dials
   above = ↑ (both levers ahead), the console below the levers = ↓ (both back),
   anywhere else = U (let go). Grim Mouse's five regions (sxfwd, sxbwd, sxleft,
   sxright, sxcancel) are gone. Proven (build/for-simon/grim16.gsv):
   build/bench/e1-up-a/b, e2-left-lever, e3-right-lever, e4-down, e5-letgo.
4. **The crane** (ew end of the world: `ew.buttonHandler`). 1998: ← → move
   the crane along its track (held), ↑ raise, ↓ lower, U or P climb out.
   **Built (15 Nov 2026):** a tap near the track (the game's own 29
   `ew.crane_points`, within 70 px on screen) is where to stop: ← (towards the
   crusher) or → held, let go a point early so the run ends on it (the game's
   `move_left` checks the key between points; its runs are cut scenes, which the
   drive doesn't count against itself). Lowered, the game raises it first
   (`raise_crane_and_move`). A tap on the crane = ↓, lowered ↑; a tap away from
   the track = U (climb out; in between the game says no). Grim Mouse's six
   regions and its `move_to_left/right` and `move_left/right` overrides are
   gone: the 1998 crane scripts run. Proven (build/for-simon/grim15.gsv): along
   the track, lowered in between, back to the conveyor (raised first), climbed
   out (build/bench/c1-b, c2-lowered, c3-b, c4-out, c5-final-move).
5. **Glottis's ride through the albinizod tunnel** (at: `at_bw_handler`).
   1998: ↑ ↓ drive (held), U the ledge (or use what's in hand), P or I
   toggle the remote, E look, 1-9 = and - the inventory hot keys.
   **Built (15 Nov 2026):** a tap is snapped to Glottis's own line along the
   tunnel (nearest on screen), ↑ (forward) or ↓ held until he's there; the game
   stops him short of the albinizod itself (blocked). The wagon hides the tunnel
   behind it, so a tap beside it, up the tunnel, backs up. A tap on the wagon =
   I (the remote), on the catwalk (the game's own `at.ledge`: Grim Mouse's
   "sxcat" region is now its outline) = U. Grim Mouse's linear mode and
   `at.linearMove*` are no longer reached (mouse.lua's are gone). Proven
   (build/for-simon/grim17.gsv): build/bench/t2-b, t5-fwd, t5-back, t6-catwalk.

**The four saves** (build/for-simon, slots 14-17), each from a new game, then
the game's own developer means, as grim13 was: grim14 "Forklift", the jump
`winecellar` (LucasArts' own, which sets the Year 2 state it needs), then out to
the elevator and back by pointer (the jump leaves the forklift dead until the
cellar is entered again); grim15 "Crane", the crane's own entry
(`ew.operate_crane`, what the cabin door's walkOut runs: there's no jump near
it); grim16 "Ship engine", the jump `hitsquad` (its cut scene skipped), then a
tap on the levers; grim17 "Tunnel ride", the jump `albinizod`. Inventory and
earlier years are whatever a new game has: they're for trying the vehicles,
not for playing on. developerMode comes from the engine's settings on every
load, so the saves carry none.

## Pushing, crawling, climbing (one axis)

6. **The wheelbarrow** (tr tree pump room: `wheelbarrow_button_handler`).
   1998: ↑ push, ↓ pull (held), U, P, I or Esc let go. Proposed: tap along
   the path = ↑ or ↓ held until there; tap the wheelbarrow or Manny = U (let
   go). Grim Mouse: linear mode plus a "go" region over the whole top of the
   screen for letting go.
   **Built (15 Nov 2026)** (HotspotMan::momentEvent, as the vehicles): the tap is
   placed on Manny's line (his facing, through where he stands, nearest on screen)
   and ↑ or ↓ is held until he's there or can go no further (the game's own
   wb_push_lim / wb_pull_lim). The wheelbarrow is the game's tr.wheelbarrow, found
   where its tr.barrow actor is drawn (linked by mouse.lua); a tap on it or on Manny
   = U. Grim Mouse's linear mode and its tr.linearMove* are retired. Proven
   (build/for-simon/grim18.gsv): build/bench/m6-pickup, m6-push, m6-pull, m6-letgo.
   (That save carried the retired script; in a new game a pull never ended, as
   Grim Mouse's tr.lua loop still asked for it: the 1998 loops are back, proof.md
   fix 15, and the same for the crawl's ac.lua.)
7. **The anchor room crawl** (ac: `drift_button_handler`). 1998: ↑ crawl
   forward, ↓ crawl back (held), E look at what Manny's facing, I "not now".
   Proposed: tap along the crawl = ↑ or ↓ held until there; two fingers = E.
   **Built (15 Nov 2026):** as the wheelbarrow, along Manny's facing; the belt's
   own current carries him back as in 1998. A tap at the anchor end crawls him into
   the game's anchor walkOut (the Lamancha). Grim Mouse's ac.linearMove* retired.
   Proven (grim19.gsv): build/bench/m7-start, m7-down2, m7-up5, m7-look, m7-fwd3
   (the anchor, then the Lamancha cut scene).
8. **Glottis hanging on the Lamancha** (gh: `drift_button_handler`). 1998: ↑ ↓
   along the hull (held), E look. Proposed: as the anchor room crawl.
   **Built:** it is the same handler and the same crawl (gh's anchor door puts
   Manny back on the ac belt under `drift_button_handler`), so line 7 covers it.
9. **The conveyor chain** (cy: `cy.drift_button_handler`). 1998: ↑ climb
   up, ↓ climb down (held), E look, I "not now". Off the belt: walk into the
   game's jump box (`cy.jump_box.walkOut`). Proposed: tap the chain above or
   below Manny = ↑ or ↓ held until level; tap the floor beside the belt =
   the jump box's walkOut, as walking into it was. Grim Mouse: an invented
   "offbelt" object that calls the same jump.
   **Built (15 Nov 2026), the chain:** the tap is placed on the chain (the game's
   own cy.chain_drift_bottom to cy.chain_drift_top), ↑ or ↓ held until level; the
   top and the bottom are the game's own ends (cv_door, end_drift_gracefully).
   Proven (grim20.gsv): build/bench/m9-start, m9-part, m9-down, m9-up (over the top
   into cv). Off the belt (the jump box) is the normal walk handler and still Grim
   Mouse's cy.offbelt: not reached on the bench, left for the playthrough.
10. **Ladders** (le ladder to the roof, sh and te ladders, si, at:
    `start_climb_ladder`, then the normal handler with `is_climbing`). 1998:
    ↑ climb up, ↓ climb down (held), stepping off at either end by itself.
    Proposed: tap the ladder above or below Manny = ↑ or ↓ held until he's
    level with the point. Grim Mouse: `climbTowards` (the same idea; it calls
    the climb scripts directly).
    **Built (15 Nov 2026):** while `is_climbing` under the normal handler, a tap
    on the ladder's line (straight up and down through Manny's middle) holds ↑ or ↓
    until he's level (the game's own climb_actor_up/down step him); he steps off
    at either end by himself. Grim Mouse's climbTowards and climb_actor_*_to
    retired. Proven on sh's ladder (grim21.gsv): build/bench/m10-on, m10-up, m10-down.

## Working a machine close up

11. **Copal's computer** (co: `co.computer.buttonHandler`). 1998: ↑ ↓ move
    through the ten replies (the list scrolls), U set the auto-reply and
    leave, P, ← → or Space hear the line, E hear the line, Esc leave.
    Proposed: point at a reply = the selection moves there (↑/↓); tap = U;
    two fingers = E; a tap on the last visible row when more replies follow
    = ↓ (scrolls, as the key did); Skip = Esc. Grim Mouse: a 6-row dialogue
    list, so replies 7 to 10 can't be reached at all (a gap today).
    **Built (15 Nov 2026):** the six rows are the game's own (co.computer.text, 40
    px apart). Pointing at a row presses ↑ or ↓ until it's the selection; a tap
    presses them and then U; a tap on the last row while more follow presses ↓ only
    (the list scrolls), on the first row while the list is scrolled ↑ only. Each
    press is held 100 ms, one at a time when the game's wait_for_joystick_release
    is done. **Replies 7-10 are reachable.** Proven (grim22.gsv): build/bench/
    m11-open, m11-hover, m11-reply10, m11-back, m11-chosen (reply 8 set, Manny leaves).
12. **The roulette panel** (cf cafe office: `roulettePanelButtonHandler`).
    1998: U throw the magnet switch, E look, Esc close. Proposed: tap the
    switch = U, two fingers = E, Skip = Esc. Grim Mouse: "sxmagnet" and
    "sxcancel" regions.
    **Built (15 Nov 2026):** a tap on the switch (Grim Mouse's sxmagnet outline,
    kept as the switch's shape) = U; two fingers = E; Skip = Esc; elsewhere nothing.
    Proven (grim23.gsv): build/bench/m12-panel, m12-look, m12-switch, m12-closed.
13. **The ticket printer** (tp, from cn: `tpButtonHandler`). 1998: ← → move
    between the week, day and race dials and the print key, ↑ ↓ push the
    dial up or down, U or E look, Esc close. Proposed: tap the upper half of
    a dial = ← or → to it, then ↑; the lower half = the same, then ↓; tap
    the print key = to it, then ↓; Skip = Esc. Grim Mouse: seven regions
    that move Manny's hands and run the push scripts directly.
    **Built (15 Nov 2026):** the dials' outlines are kept as shapes; a tap presses
    ← or → (the shorter way round, as tp.move_left/right go) until the hands are on
    that dial, then ↑ or ↓; the print key = to it, then ↓. Proven (grim24.gsv):
    build/bench/m13-start, m13-week-up2 (week 03), m13-day-down, m13-print (ticket
    printed, back at the track).
14. **The vault door wheel** (vd: `vd.buttonHandler`). 1998: → turn
    clockwise, ← counter-clockwise, ↓ or Esc step back. Proposed: tap the
    wheel's right half = →, its left half = ←, Skip = Esc. Grim Mouse: the
    same as three regions (left and right swapped against the keys: check).
    **Built (15 Nov 2026):** the wheel's right half = →, left half = ← (by the
    close-up's outlines, or on the wide view by the game's own vd.wheel point),
    held for as long as the finger is down (a tap is a short press: one 45-degree
    turn before the door is drilled; after it, a press and hold spins the tumblers,
    as holding the key did); Skip = Esc. Grim Mouse's direction was swapped and is
    gone. Proven (grim25.gsv): build/bench/m14-wheel, m14-right, m14-left, m14-off.
    Not proven on the bench: the drilled door's spin.
15. **The broadaxe** (vo outer vault: `axeButtonHandler`). 1998: ← → turn
    (held), ↓ walk backwards (held), U drop the axe, P or Esc lower it, E
    look. Proposed: tap the floor = ← or → held until Manny's back is to the
    point, then ↓ held until he's there; tap the axe = U; two fingers = E;
    Skip = Esc. Grim Mouse: an invented "broadaxe" object (drop only).
    **Built (15 Nov 2026):** a tap on the floor: ← or → held until his back is to
    the point (the game's vo.turn_left/right), then ↓ held until he's there; a tap
    on Manny = U (drop). Proven (grim26.gsv): build/bench/m15-turn, m15-backed,
    m15-look, m15-drop. Grim Mouse's vo.dummy_axe is no longer reached.
16. **The fire extinguisher** (bd beaver dam: `fireExtinguisherHandler`).
    1998: hold U to spray, let go to stop. Proposed: press and hold on the
    scene = U held, lift = U released. Grim Mouse: a tap toggles spraying.
    **Built (15 Nov 2026), as decided:** with the extinguisher in hand in bd, a
    press held (the app's hold, 0.4 s) is U held: the game's own
    bd.extinguisher.use (Grim Mouse's toggle and start_ext are retired); lifting
    lets U go, which the game's fireExtinguisherHandler hears. A quick tap is the
    usual pointer (walk, look, objects). Proven (grim27.gsv): build/bench/
    m16-holding, m16-spray, m16-stopped, m16-tapwalk.
17. **The rope on the ledge** (le: `ledge_rope_button_handler`). 1998: U
    throw the rope, P drop it, E look at it, I the rope's own inventory.
    Proposed: tap where to throw = U, two fingers = E, tap Manny = I. **Open:**
    P (drop the rope) has no gesture under the rules. Simon to choose: tap
    the rope coil at Manny's feet, or leave P out (throwing is the puzzle).
    **Built (15 Nov 2026), P left out as decided:** tap = U (throw), two fingers =
    E, a tap on Manny = I. Found on the way: Grim Mouse's le.lua threw (or dropped)
    the rope the moment it was picked up, so this handler was never reached; the
    1998 pick-up is back (le.lua.patchr now carries only the two stop_walk fixes).
    Proven (grim28.gsv): build/bench/m17-holding, m17-look, m17-throw (a miss: the
    coral isn't tied).

## One key and it's over

18. **Manny sprouting in the meadow** (mf: `dead_button_handler`). 1998: any
    arrow = flail, U or P = the wound (or what's in hand), E look at it, I
    the coat. Proposed: tap the ground = ↑ (flail); tap the wound = U; two
    fingers = E; tap Manny = I. Grim Mouse: "no walk" mode (any tap flails)
    and makes the wound touchable for good.
    **Built (15 Nov 2026):** the wound's outline = U, Manny as drawn = I, elsewhere
    ↑ (flail), two fingers = E. Proven (grim29.gsv): build/bench/m18-flail,
    m18-look, m18-wound.
19. **Getting up from the cold** (re rubamat exterior: `shiver_button_handler`).
    1998: any key gets Manny up. Proposed: a tap anywhere = U.
    **Built (15 Nov 2026):** a tap anywhere = U. Found on the way: Grim Mouse's
    re.lua got Manny up by itself at the end of the intro, so the moment never
    came; re.lua is the 1998 one again (its patch held nothing else). Proven from
    the game's own jump `plunge` (grim30.gsv): build/bench/m19-up.
20. **The camera at the new headquarters** (nq: `camera_button_handler`).
    1998: any key leaves the camera. Proposed: a tap anywhere = U.
    **Built (15 Nov 2026):** a tap anywhere = U. Proven (grim31.gsv): build/bench/m20-back.
21. **The photo finish** (pf: `pfButtonHandler`). 1998: any key goes back.
    Proposed: a tap anywhere = U. (Grim Mouse: the same.)
    **Built (15 Nov 2026):** a tap anywhere = U (Grim Mouse's pf.mouseSpecial
    retired). Proven (grim32.gsv): build/bench/m21-back.

## Two scenes with their own hand-over

22. **Handing Chepito to Glottis** (su sunken Lola: `suButtonHandler`, after
    Manny grabs the lantern). 1998: ← or → hands Chepito over. Proposed: tap
    Glottis = → . Grim Mouse: a two-line pick ("lantern", "Glottis") drawn as
    a dialogue: a menu, so dropped.
    **Built (15 Nov 2026):** a tap on Glottis as drawn = →; elsewhere nothing. The
    lantern is grabbed by a normal tap on it. Proven (grim33.gsv): build/bench/
    m22-grab, m22-handover, m22-after.

## Dialogue with its own keys

23. **The elevator operator** (ly Le Mans lobby, `dlg_brennis2`:
    `br2.buttonHandler`). 1998: the dialogue keys (↑ ↓ a line, Page Up/Down
    four lines, Enter choose) over a list that scrolls. Proposed: as every
    dialogue (point at a line, tap = choose), with a tap on the last visible
    line when more follow = ↓ (scrolls). Grim Mouse: "dxup"/"dxdown" calling
    the lift directly.
    **Built (15 Nov 2026):** the four rows (as Grim Mouse lays the list out) are
    the game's floors: a tap presses ↓ or ↑ until that floor is the current line,
    then Enter; on the last row while more follow, ↓ only (the game puts the
    current line at the top, so the list moves on three); just above the list ↑
    (one back), just below ↓. Pointing doesn't move the line (each ↓ scrolls).
    Proven (grim34.gsv): build/bench/m23-list, m23-scrolled, m23-scrolled2,
    m23-chosen ("eight": Brennis's "sorry"), m23-up. Grim Mouse's arrow images
    aren't drawn, so the way back above the list is unmarked: for Simon.
24. **The poetry reading** (bi, `dlg_mic`): the normal dialogue keys under
    its own handler. Proposed: as every dialogue. Nothing new.
    **Proven (15 Nov 2026)** (grim35.gsv): build/bench/m24-lines, m24-hover, m24-chosen.

## Not the player's controls at all

25. **The fire extinguisher's save** (bd), **the porthole views** (dp, op,
    ul) and the scripts that hand back `inventory_save_handler`: they only
    put the previous handler back. Nothing to design.
26. **The scythe on the Bone Wagon's road** (lb, bv, bd set the Bone Wagon
    handler on entry): covered by line 1.

## Decided (Simon, 15 Nov 2026)

- Line 16, the fire extinguisher: **press and hold to spray**, lift to stop.
- Line 17, the rope: **drop is left out**; throwing is the puzzle.
- Lines 19-21, the "any key" scenes: **a tap anywhere** moves on.
- Vehicles (1-5): **tap where to go** (Simon tried the Bone Wagon: "It's not a
  driving experience, the point and click just works"); the ship's engine keeps
  its levers. All five built (15 Nov 2026). Open: the Bone Wagon's turning is
  slow at the 1998 rate (line 1); whether to keep the gas held through turns.

## For Simon to decide (as proposed)

- Line 16, press and hold: the only hold gesture in Grim. It is what the
  original asked of the player (hold U), but it's new to PointyClicky.
- Line 17, the rope's P.
- The three "any key" scenes (19-21): U is proposed so that a tap is always
  "the main action".
