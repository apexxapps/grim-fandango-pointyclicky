# The moments the game takes the controls: proposals for Simon

*Not built. For Simon to approve, line by line (15 Nov 2026).*

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
  A tap on Manny is the coat (I), or with something in hand puts it away (P).
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
2. **Forklift** (de dillopede elevator, wc wine cellar:
   `forklift_button_handler`). 1998: ↑ forward, ↓ back (out of the shaft when
   stuck), ← → turn, U or P dismount. Proposed: as the Bone Wagon (tap ground
   ahead = ↑ and steering held until there, behind = ↓, tap the forklift = U).
   Grim Mouse: invented `de.forkdrive` and `wc.forkdrive`.
3. **The ship's engine** (ei engine room: `engineButtonHandler`). 1998: ↑
   ahead, ↓ reverse, ← port, → starboard (each press runs one `drive_ship`),
   U, P or I let go of the controls. Proposed: tap the left lever = ←, the
   right lever = →, the dial or the forward half of the controls = ↑, the
   back half = ↓, tap Manny = U (let go). Grim Mouse: five screen regions
   (sxfwd, sxbwd, sxleft, sxright, sxcancel).
4. **The crane** (ew end of the world: `ew.buttonHandler`). 1998: ← → move
   the crane along its track (held), ↑ raise, ↓ lower, U or P climb out.
   Proposed: tap a point along the track = ← or → held until the crane is
   over it; tap the hook while it's up = ↓, while it's down = ↑; tap Manny =
   U. Grim Mouse: six screen regions that also raise and lower on arrival
   (one gesture doing two things: dropped).
5. **Glottis's ride through the albinizod tunnel** (at: `at_bw_handler`).
   1998: ↑ ↓ drive (held), U the ledge (or use what's in hand), P or I
   toggle the remote, E look, 1-9 = and - the inventory hot keys. Proposed:
   tap along the tunnel = ↑ or ↓ held until there; tap the ledge = U; tap
   Manny = I (the remote). Grim Mouse: linear mode and a "sxcat" region.

## Pushing, crawling, climbing (one axis)

6. **The wheelbarrow** (tr tree pump room: `wheelbarrow_button_handler`).
   1998: ↑ push, ↓ pull (held), U, P, I or Esc let go. Proposed: tap along
   the path = ↑ or ↓ held until there; tap the wheelbarrow or Manny = U (let
   go). Grim Mouse: linear mode plus a "go" region over the whole top of the
   screen for letting go.
7. **The anchor room crawl** (ac: `drift_button_handler`). 1998: ↑ crawl
   forward, ↓ crawl back (held), E look at what Manny's facing, I "not now".
   Proposed: tap along the crawl = ↑ or ↓ held until there; two fingers = E.
8. **Glottis hanging on the Lamancha** (gh: `drift_button_handler`). 1998: ↑ ↓
   along the hull (held), E look. Proposed: as the anchor room crawl.
9. **The conveyor chain** (cy: `cy.drift_button_handler`). 1998: ↑ climb
   up, ↓ climb down (held), E look, I "not now". Off the belt: walk into the
   game's jump box (`cy.jump_box.walkOut`). Proposed: tap the chain above or
   below Manny = ↑ or ↓ held until level; tap the floor beside the belt =
   the jump box's walkOut, as walking into it was. Grim Mouse: an invented
   "offbelt" object that calls the same jump.
10. **Ladders** (le ladder to the roof, sh and te ladders, si, at:
    `start_climb_ladder`, then the normal handler with `is_climbing`). 1998:
    ↑ climb up, ↓ climb down (held), stepping off at either end by itself.
    Proposed: tap the ladder above or below Manny = ↑ or ↓ held until he's
    level with the point. Grim Mouse: `climbTowards` (the same idea; it calls
    the climb scripts directly).

## Working a machine close up

11. **Copal's computer** (co: `co.computer.buttonHandler`). 1998: ↑ ↓ move
    through the ten replies (the list scrolls), U set the auto-reply and
    leave, P, ← → or Space hear the line, E hear the line, Esc leave.
    Proposed: point at a reply = the selection moves there (↑/↓); tap = U;
    two fingers = E; a tap on the last visible row when more replies follow
    = ↓ (scrolls, as the key did); Skip = Esc. Grim Mouse: a 6-row dialogue
    list, so replies 7 to 10 can't be reached at all (a gap today).
12. **The roulette panel** (cf cafe office: `roulettePanelButtonHandler`).
    1998: U throw the magnet switch, E look, Esc close. Proposed: tap the
    switch = U, two fingers = E, Skip = Esc. Grim Mouse: "sxmagnet" and
    "sxcancel" regions.
13. **The ticket printer** (tp, from cn: `tpButtonHandler`). 1998: ← → move
    between the week, day and race dials and the print key, ↑ ↓ push the
    dial up or down, U or E look, Esc close. Proposed: tap the upper half of
    a dial = ← or → to it, then ↑; the lower half = the same, then ↓; tap
    the print key = to it, then ↓; Skip = Esc. Grim Mouse: seven regions
    that move Manny's hands and run the push scripts directly.
14. **The vault door wheel** (vd: `vd.buttonHandler`). 1998: → turn
    clockwise, ← counter-clockwise, ↓ or Esc step back. Proposed: tap the
    wheel's right half = →, its left half = ←, Skip = Esc. Grim Mouse: the
    same as three regions (left and right swapped against the keys: check).
15. **The broadaxe** (vo outer vault: `axeButtonHandler`). 1998: ← → turn
    (held), ↓ walk backwards (held), U drop the axe, P or Esc lower it, E
    look. Proposed: tap the floor = ← or → held until Manny's back is to the
    point, then ↓ held until he's there; tap the axe = U; two fingers = E;
    Skip = Esc. Grim Mouse: an invented "broadaxe" object (drop only).
16. **The fire extinguisher** (bd beaver dam: `fireExtinguisherHandler`).
    1998: hold U to spray, let go to stop. Proposed: press and hold on the
    scene = U held, lift = U released. Grim Mouse: a tap toggles spraying.
17. **The rope on the ledge** (le: `ledge_rope_button_handler`). 1998: U
    throw the rope, P drop it, E look at it, I the rope's own inventory.
    Proposed: tap where to throw = U, two fingers = E, tap Manny = I. **Open:**
    P (drop the rope) has no gesture under the rules. Simon to choose: tap
    the rope coil at Manny's feet, or leave P out (throwing is the puzzle).

## One key and it's over

18. **Manny sprouting in the meadow** (mf: `dead_button_handler`). 1998: any
    arrow = flail, U or P = the wound (or what's in hand), E look at it, I
    the coat. Proposed: tap the ground = ↑ (flail); tap the wound = U; two
    fingers = E; tap Manny = I. Grim Mouse: "no walk" mode (any tap flails)
    and makes the wound touchable for good.
19. **Getting up from the cold** (re rubamat exterior: `shiver_button_handler`).
    1998: any key gets Manny up. Proposed: a tap anywhere = U.
20. **The camera at the new headquarters** (nq: `camera_button_handler`).
    1998: any key leaves the camera. Proposed: a tap anywhere = U.
21. **The photo finish** (pf: `pfButtonHandler`). 1998: any key goes back.
    Proposed: a tap anywhere = U. (Grim Mouse: the same.)

## Two scenes with their own hand-over

22. **Handing Chepito to Glottis** (su sunken Lola: `suButtonHandler`, after
    Manny grabs the lantern). 1998: ← or → hands Chepito over. Proposed: tap
    Glottis = → . Grim Mouse: a two-line pick ("lantern", "Glottis") drawn as
    a dialogue: a menu, so dropped.

## Dialogue with its own keys

23. **The elevator operator** (ly Le Mans lobby, `dlg_brennis2`:
    `br2.buttonHandler`). 1998: the dialogue keys (↑ ↓ a line, Page Up/Down
    four lines, Enter choose) over a list that scrolls. Proposed: as every
    dialogue (point at a line, tap = choose), with a tap on the last visible
    line when more follow = ↓ (scrolls). Grim Mouse: "dxup"/"dxdown" calling
    the lift directly.
24. **The poetry reading** (bi, `dlg_mic`): the normal dialogue keys under
    its own handler. Proposed: as every dialogue. Nothing new.

## Not the player's controls at all

25. **The fire extinguisher's save** (bd), **the porthole views** (dp, op,
    ul) and the scripts that hand back `inventory_save_handler`: they only
    put the previous handler back. Nothing to design.
26. **The scythe on the Bone Wagon's road** (lb, bv, bd set the Bone Wagon
    handler on entry): covered by line 1.

## For Simon to decide

- The vehicle rule (lines 1-5): "tap where to go, the game's own arrows are
  held until it's there". One rule for the Bone Wagon, the forklift and the
  crane; the ship's engine stays on its levers because that's what the
  player works in that scene.
- Line 16, press and hold: the only hold gesture in Grim. It is what the
  original asked of the player (hold U), but it's new to PointyClicky.
- Line 17, the rope's P.
- The three "any key" scenes (19-21): U is proposed so that a tap is always
  "the main action".
