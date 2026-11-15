PrintDebug("sourced mouse.lua") -- Grim Mouse mouse.lua, (c) Tobias Pfaff, GPL-2.0-or-later;
-- decompiled from mouse.lab bytecode with scummvm-tools delua on 2026-11-11
-- PointyClicky Edition (15 Nov 2026): this file runs at boot AND again after
-- every load (the engine re-runs it, so a save made before a fix gets the fix).
-- So every top-level statement must be harmless the second time: functions and
-- constant fields are simply set again; an object is created only if it isn't
-- there (its touchable state is the save's); a rename only if the name differs
-- (a second RenameHotspot would give the hotspot a new id and unlink its outline);
-- a function we wrap is captured once (pc_*).
system.mouseCommand = function(arg1, arg2, arg3) -- line 3
    if system.currentSet then
        system.currentSet:mouseCommand(arg1, arg2, arg3)
    end
end
system.mouseSpecial = function(arg1, arg2) -- line 8
    if system.currentSet then
        if system.currentSet.mouseSpecial then
            system.currentSet:mouseSpecial(arg1, arg2)
        end
    end
end
system.mouseWalk = function(arg1, arg2, arg3, arg4) -- line 15
    if system.currentSet then
        system.currentSet:mouseWalk(arg1, arg2, arg3 / 3, arg4)
    end
end
system.mouseUseInHand = function(arg1, arg2) -- line 20
    if system.currentSet and system.currentActor and system.currentActor.is_holding then
        system.currentSet:mouseWalk(arg1, arg2, 0, nil)
    end
end
-- PointyClicky Edition (Simon, 15 Nov 2026): with something in hand, a tap on
-- Manny is the 1998 U with nothing hot (_controls.lua's last USE branch): the
-- held thing used on its own (Manny bites the mouthpiece, plants the sign).
-- Putting it away is the game's own P (the app's swipe up). This replaces Grim
-- Mouse's hidden binding, a two-finger tap on the floor (just_walk, below).
system.mouseUseHeld = function() -- PointyClicky Edition
    if cutSceneLevel > 0 or not system.currentActor or not system.currentActor.is_holding then
        return
    end
    system.currentActor.stop_idle = TRUE
    kill_soft_scripts()
    stop_script(walk_and_do)
    stop_script(just_walk)
    stop_script(Sentence)
    start_script(Sentence, "use", system.currentActor.is_holding)
end
system.dialogSelect = function(arg1, arg2) -- line 25
    -- (PointyClicky Edition: Copal's computer and the elevator's floors are
    -- worked by their own keys, which the engine sends: docs/moments.md 11, 23)
    if co and system.buttonHandler == co.computer or br2 and system.buttonHandler == br2 then
        return
    end
    if system.lastDialog then
        system.lastDialog:mouseSelect(arg1, arg2)
    end
end
system.mouseInventory = function(name, button) -- line 30
    if arg1 == "outside" then -- sic: the bytecode reads the GLOBAL arg1 here, not the parameter
        manny.is_holding = nil
        Inventory:close_me()
    else
        item = Inventory:get_item(name)
        if button == 1 or button == 3 then
            manny.is_holding = item
            Inventory:close_me()
        elseif button == 2 then
            start_script(Sentence, "lookAt", item)
        end
    end
end
system.mouseNowalk = function(arg1) -- line 44
    if system.currentSet and system.currentSet.nowalk then
        system.currentSet:nowalk(arg1)
    end
end
-- PointyClicky Edition (15 Nov 2026): characters' live outlines. An object
-- that stands for a character is the game's X_obj for its actor X (glottis_obj,
-- meche_obj...); the engine then finds it where the character is drawn. Where the
-- game's scripts tie one to an actor of another name, that's here: pi.lua moves
-- terry_obj with terry, at.lua albinizod_obj with zod, su.lua moving_chepito_obj
-- with chepito; Maximino and the Gate Keeper are maximino and gate_keeper.
pc_actor_of = { terry_obj = "terry", albinizod_obj = "zod", moving_chepito_obj = "chepito", max_obj = "maximino", keeper_obj = "gate_keeper" }
pc_link_actors = function(arg1)
    local local1, local2, local3, local4
    local1, local2 = next(arg1, nil)
    while local1 do
        if type(local1) == "string" and type(local2) == "table" and local2.hotspot_id and strlen(local1) > 4 and strsub(local1, strlen(local1) - 3) == "_obj" then
            local3 = pc_actor_of[local1] or strsub(local1, 1, strlen(local1) - 4)
            local4 = getglobal(local3)
            if type(local4) == "table" and local4.hActor then
                LinkHotspotActor(local2.hotspot_id, local4.hActor)
            end
        end
        local1, local2 = next(arg1, local1)
    end
    pc_link_vehicles(arg1)
end
-- PointyClicky Edition (15 Nov 2026): the vehicles are the game's own objects,
-- found where the vehicle is drawn. The game itself moves these objects' use
-- points to where the vehicle was left (sg.leave_BW, the forklift's dismount),
-- so with the link a tap on the parked Bone Wagon or forklift gets Manny in,
-- wherever it is. (Grim Mouse's invented sg/na.bone_drive and de/wc.forkdrive
-- are gone; saves made with them keep theirs, with no outline.)
pc_link_vehicles = function(arg1)
    local local1
    if type(arg1.bone_wagon) == "table" and arg1.bone_wagon.hotspot_id then
        local1 = bonewagon
        if arg1 == at then
            local1 = glottis
        end
        if type(local1) == "table" and local1.hActor then
            LinkHotspotActor(arg1.bone_wagon.hotspot_id, local1.hActor)
        end
    end
    -- (the forklift is live wherever it's drawn: de.forklift_actor.monitor_objects
    -- flips its touchable flag and the lever's by which is nearer Manny, which
    -- picks the keyboard's hot object, not what a pointer may touch)
    if type(arg1.forklift) == "table" and arg1.forklift.hotspot_id and de.forklift_actor.hActor then
        LinkHotspotActor(arg1.forklift.hotspot_id, de.forklift_actor.hActor, TRUE)
    end
    -- the sign post in the clearing is the game's signpost actor, standing
    -- wherever Manny planted it (its outline was a strip right across the screen,
    -- so a tap on the floor anywhere in that band went to the sign: proof F18)
    if arg1 == na and type(na.signpost) == "table" and na.signpost.hotspot_id and type(signpost) == "table" and signpost.hActor then
        LinkHotspotActor(na.signpost.hotspot_id, signpost.hActor)
    end
    -- the wheelbarrow is the game's tr.wheelbarrow, drawn by its tr.barrow actor
    -- (pushed about by the wheelbarrow's own keys, docs/moments.md line 6)
    if arg1 == tr and type(tr.barrow) == "table" and tr.barrow.hActor and tr.wheelbarrow.hotspot_id then
        LinkHotspotActor(tr.wheelbarrow.hotspot_id, tr.barrow.hActor, TRUE)
    end
end
Set.update_hotspots = function(arg1) -- line 69
    local local1, local2
    break_here()
    pc_link_actors(arg1)
    local1, local2 = next(arg1, nil)
    ActivateHotspot(-1, FALSE)
    while local1 do
        -- (PointyClicky Edition: a touchable table with no range or hotspot,
        -- as the wine cellar has, stopped this loop with an error, and every
        -- object after it in the set stayed dead: the forklift, for one)
        if type(local2) == "table" then
            if local2.touchable and local2.hotspot_id and type(local2.range) == "number" and local2.range > 0 then
                ActivateHotspot(local2.hotspot_id, TRUE)
            end
        end
        local1, local2 = next(arg1, local1)
    end
end
walk_and_do = function(arg1, arg2, arg3, arg4, arg5) -- line 83
    if cutSceneLevel > 0 then
        return
    end
    if system.currentActor.driveto then
        local local1, local2, local3
        local1 = arg2.use_pnt_x
        local2 = arg2.use_pnt_y
        local3 = arg2.use_pnt_z
        if local1 and not arg2.active_driving then
            system.currentActor:driveto(local1, local2, local3)
        end
    elseif not arg2.use_immediate then
        if arg4 == 2 then
            result = system.currentActor:runto_object(arg2, nil, 0)
        elseif arg4 == 1 then
            result = system.currentActor:walkto_object(arg2, nil, 0)
        end
    end
    if cutSceneLevel > 0 then
        return
    end
    if arg3 == 4 or arg3 == 5 then
        if not arg2.walkOut then
            arg1 = "lookAt"
            NotifyWalk(arg2.hotspot_id)
        end
    end
    if system.currentActor == manny or arg2.active_driving then
        Sentence(arg1, arg2, arg5)
    else
        WalkActorForward(system.currentActor.hActor)
    end
end
just_walk = function(arg1, arg2, arg3) -- line 117
    if cutSceneLevel > 0 then
        return
    end
    local local1 = 0
    -- (PointyClicky Edition, 15 Nov 2026: Grim Mouse's two-finger tap on the
    -- floor with something in hand, which walked there and used it, is retired;
    -- a tap on Manny does that now: system.mouseUseHeld. Two fingers only look.)
    while local1 < arg2 do
        local local2 = arg3[local1 * 3]
        local local3 = arg3[local1 * 3 + 1]
        local local4 = arg3[local1 * 3 + 2]
        if system.currentActor.driveto then
            system.currentActor:driveto(local2, local3, local4)
        else
            WalkActorTo(system.currentActor.hActor, local2, local3, local4, nil, nil, nil, 0)
        end
        system.currentActor:wait_for_actor()
        local1 = local1 + 1
    end
    if system.currentActor.driveto then
        WalkActorForward(system.currentActor.hActor)
    end
end
Set.mouseWalk = function(arg1, arg2, arg3, arg4, arg5) -- line 143
    if cutSceneLevel > 0 then
        return
    end
    system.currentActor.stop_idle = TRUE
    kill_soft_scripts()
    stop_script(Sentence)
    stop_script(walk_and_do)
    stop_script(just_walk)
    if arg3 == 0 then
        system.currentActor:set_run(FALSE)
    else
        system.currentActor:set_run(TRUE)
    end
    if system.currentActor.set_walk_backwards then
        system.currentActor:set_walk_backwards(FALSE)
    end
    start_script(just_walk, arg2, arg4, arg5)
end
Set.mouseCommand = function(arg1, arg2, arg3, arg4) -- line 162
    local local1, local2
    if cutSceneLevel > 0 then
        return
    end
    system.currentActor.stop_idle = TRUE
    local1, local2 = next(arg1, nil)
    while local1 do
        if type(local2) == "table" then
            if local2.hotspot_id == arg3 then
                kill_soft_scripts()
                stop_script(walk_and_do)
                stop_script(just_walk)
                stop_script(Sentence)
                if arg2 == 2 then
                    start_script(walk_and_do, "lookAt", local2, arg2, arg4)
                elseif arg2 == 1 or arg2 == 4 or arg2 == 5 then
                    if local2.walkOut and (not system.currentActor.is_holding or not system.currentActor.is_holding.use_on_door) then
                        start_script(walk_and_do, "walkOut", local2, arg2, arg4)
                    elseif system.currentActor.is_holding then
                        start_script(walk_and_do, "use", local2, arg2, arg4, system.currentActor.is_holding)
                    else
                        start_script(walk_and_do, "use", local2, arg2, arg4)
                    end
                elseif arg2 == 3 then
                    if system.currentActor.is_holding then
                        start_script(system.currentActor.is_holding.put_away, system.currentActor.is_holding)
                    else
                        start_script(walk_and_do, "pickUp", local2, arg2, arg4)
                    end
                end
            end
        end
        local1, local2 = next(arg1, local1)
    end
end
system.mouseOpt = function(arg1, arg2, arg3, arg4) -- line 198
    if arg1 == "op_main.set" then
        main_menu:choose_item(arg3)
    elseif arg1 == "op_help.set" then
        if arg3 == 0 then
            help_menu:cancel(TRUE)
            main_menu:run()
        elseif arg3 == 1 then
            help_menu.cur_page = help_menu.cur_page - 1
            if help_menu.cur_page < 1 then
                help_menu.cur_page = 3
            end
        elseif arg3 == 2 then
            help_menu.cur_page = help_menu.cur_page + 1
            if help_menu.cur_page > 3 then
                help_menu.cur_page = 1
            end
        end
    elseif arg1 == "op_opt.set" then
        inc = 5
        if arg3 == 13 then
            inc = 1
        end
        if arg2 == "oxlo" then
            settings_menu.gauges[arg3]:set_value(settings_menu.gauges[arg3].value - inc)
        elseif arg2 == "oxhi" then
            settings_menu.gauges[arg3]:set_value(settings_menu.gauges[arg3].value + inc)
        elseif arg2 == "oxchange" or arg2 == "oxselect" then
            settings_menu:choose_item(arg3)
        end
    elseif arg1 == "op_3d.set" then
        if arg3 > 0 then
            display_menu:choose_item(arg3)
        end
    elseif arg1 == "op_load.set" and not saveload_menu.edit_line.is_active then
        if arg2 == "oxup" then
            saveload_menu.menu.top_item = saveload_menu.menu.top_item - 3
            if saveload_menu.menu.top_item < 1 then
                saveload_menu.menu.top_item = 1
            end
        elseif arg2 == "oxdn" then
            saveload_menu.menu.top_item = saveload_menu.menu.top_item + 3
            if saveload_menu.menu.top_item + saveload_menu.menu.visible_items > saveload_menu.menu.num_items + 1 then
                saveload_menu.menu.top_item = saveload_menu.menu.num_items - saveload_menu.menu.visible_items + 1
            end
        end
        system.mouseHover(arg1, arg3)
        if arg2 == "oxselect" then
            saveload_menu:buttonHandler(13, 1, 1)
        elseif arg2 == "oxcancel" then
            saveload_menu:buttonHandler(27, 1, 1)
        end
    elseif arg1 == "op_query.set" and arg3 >= 0 and cur_query then
        system.mouseHover(arg1, arg3)
        single_start_script(cur_query.ok, cur_query)
    elseif arg1 == "op_dialog.set" then
        if arg2 == "oxup" then
            single_start_script(dialog_log.scroll_up, dialog_log)
        elseif arg2 == "oxdn" then
            single_start_script(dialog_log.scroll_down, dialog_log)
        elseif arg2 == "oxexit" then
            dialog_log:cancel(TRUE)
            main_menu:run()
        end
    elseif arg1 == "op_cut.set" then
        if arg2 == "oxup" then
            cutscene_menu.menu.top_item = cutscene_menu.menu.top_item - 3
            if cutscene_menu.menu.top_item < 1 then
                cutscene_menu.menu.top_item = 1
            end
        elseif arg2 == "oxdn" then
            cutscene_menu.menu.top_item = cutscene_menu.menu.top_item + 3
            if cutscene_menu.menu.top_item + cutscene_menu.menu.visible_items > cutscene_menu.menu.num_items + 1 then
                cutscene_menu.menu.top_item = cutscene_menu.menu.num_items - cutscene_menu.menu.visible_items + 1
            end
        end
        system.mouseHover(arg1, arg3)
        if arg2 == "oxselect" then
            cutscene_menu:buttonHandler(13, 1, 1)
        elseif arg2 == "exexit" then
            cutscene_menu:buttonHandler(27, 1, 1)
        end
    end
end
system.mouseHover = function(arg1, arg2) -- line 282
    if arg1 == "op_main.set" then
        main_menu.menu.cur_item = arg2
    elseif arg1 == "op_opt.set" then
        settings_menu.menu.cur_item = arg2
    elseif arg1 == "op_3d.set" and arg2 > 0 then
        display_menu.active_menu.cur_item = arg2
    elseif arg1 == "op_load.set" and arg2 > 0 and arg2 + saveload_menu.menu.top_item ~= saveload_menu.menu.num_items then
        if not saveload_menu.edit_line.is_active then
            saveload_menu.menu.cur_item = arg2 + saveload_menu.menu.top_item - 1
        end
    elseif arg1 == "op_query.set" and cur_query then
        cur_query.current_choice = arg2 - 1
    elseif arg1 == "op_cut.set" and arg2 > 0 and arg2 + cutscene_menu.menu.top_item ~= cutscene_menu.menu.num_items then
        cutscene_menu.menu.cur_item = arg2 + cutscene_menu.menu.top_item - 1
    end
end
suitInventoryButtonHandler2 = function(arg1, arg2, arg3) -- line 299
    if control_map.OVERRIDE[arg1] or control_map.INVENTORY[arg1] and arg2 then
        system.currentActor.is_holding = nil
        if manny.dying then
            start_script(dead_close_inventory, TRUE)
        else
            start_script(close_inventory, TRUE)
        end
    end
end
Inventory.setup_draw = function(arg1) -- line 309
    local local1
    local local2, local3
    if IsMoviePlaying() then
        StopMovie()
    else
        system.loopingMovie = nil
    end
    system.lastSet = system.currentSet
    LockSet(system.currentSet.setFile)
    if manny.costume_state == "suit" then
        local1 = suit_inv
    elseif manny.costume_state == "action" then
        local1 = action_inv
    elseif manny.costume_state == "cafe" then
        local1 = cafe_inv
    elseif manny.costume_state == "nautical" then
        local1 = nautical_inv
    elseif manny.costume_state == "siberian" or manny.costume_state == "thunder" then
        if manny.fancy then
            local1 = charlie_inv
        else
            local1 = siberian_inv
        end
    elseif manny.costume_state == "reaper" then
        local1 = death_inv
    end
    local2, local3 = next(Inventory.unordered_inventory_table, nil)
    RegisterInventory("reset")
    while local2 do
        RegisterInventory(local2.name, local2:get_inv())
        local2, local3 = next(Inventory.unordered_inventory_table, local2)
    end
end
Inventory.get_item = function(arg1, arg2) -- line 343
    local2, local3 = next(Inventory.unordered_inventory_table, nil)
    while local2 do
        if local2.name == arg2 then
            return local2
        end
        local2, local3 = next(Inventory.unordered_inventory_table, local2)
    end
    return nil
end
Inventory.userPaintHandler = function(arg1) -- line 353
    CleanBuffer()
    Display()
end
Inventory.unload_inventory = function(arg1) -- line 357
    PrintDebug("leaving inventory")
    if system.loopingMovie and type(system.loopingMovie) == "table" then
        play_movie_looping(system.loopingMovie.name, system.loopingMovie.x, system.loopingMovie.y)
    end
    if system.currentSet == sh or system.currentSet == zw then
        sh:set_up_flowers()
    end
end
Inventory.close_me = function(arg1) -- line 366
    if manny.dying then
        start_script(dead_close_inventory)
    else
        start_script(close_inventory)
    end
end
Object.rename = function(arg1, arg2) -- line 373
    arg1.name = arg2
    arg1.string_name = trim_header(arg2)
    RenameHotspot(arg1.hotspot_id, arg2)
end
-- (run again: a no-op, see the top)
pc_rename = function(arg1, arg2)
    if arg1 and arg1.name ~= arg2 then
        arg1:rename(arg2)
    end
end
Object.get_inv = function(arg1) -- line 378
    if arg1.inv_name then
        return arg1.inv_name
    else
        return arg1.string_name
    end
end
Actor.runto_object = function(arg1, arg2, arg3, arg4) -- line 385
    local local1, local2, local3, local4, local5, local6, local7
    local local8, local9
    arg1:set_run(TRUE)
    if arg1.set_walk_backwards then
        arg1:set_walk_backwards(FALSE)
    end
    if arg2.parent == Ladder then
        if arg3 then
            local9 = arg2.base.out_pnt_z
            local8 = arg2.top.out_pnt_z
        else
            local9 = arg2.base.use_pnt_z
            local8 = arg2.top.use_pnt_z
        end
        local1 = arg1:getpos()
        if abs(local9 - local1.z) < abs(local8 - local1.z) then
            arg2 = arg2.base
        else
            arg2 = arg2.top
        end
    end
    local2 = arg2.use_pnt_x
    local3 = arg2.use_pnt_y
    local4 = arg2.use_pnt_z
    local5 = arg2.use_rot_x
    local6 = arg2.use_rot_y
    local7 = arg2.use_rot_z
    if local2 then
        PrintDebug("Run " .. arg1.name .. " to " .. arg2.name .. "\t" .. local2 .. "\t" .. local3 .. "\t" .. local4 .. "\n")
        if arg1 == system.currentActor then
            stop_movement_scripts()
        end
        SetActorConstrain(arg1.hActor, FALSE)
        arg1:runto(local2, local3, local4, local5, local6, local7, arg4)
        while arg1:is_moving() or arg1:is_turning() do
            break_here()
        end
        if arg1 == system.currentActor and MarioControl then
            WalkVector.x = 0
            WalkVector.y = 0
            WalkVector.z = 0
            single_start_script(WalkManny)
        end
        local1 = object_proximity(arg2, arg3)
        if local1 <= MAX_PROX then
            PrintDebug("made it to the use/out point of " .. arg2.name .. "!\n")
            return TRUE
        else
            PrintDebug("Didn't make it to the use/out point of " .. arg2.name .. "!\n")
            return FALSE
        end
    else
        PrintDebug("Object has no use/out point!\n")
    end
end
Actor.set_walk_chore = function(arg1, arg2, arg3, arg4) -- line 441
    arg1.walk_chore = arg2
    if not arg3 then
        arg3 = arg1.base_costume
    end
    SetActorWalkChore(arg1.hActor, arg2, arg3, arg4)
end
Actor.setpos = function(arg1, arg2, arg3, arg4, arg5) -- line 448
    if type(arg2) == "table" then
        arg1:moveto(arg2.x, arg2.y, arg2.z, arg5)
    else
        arg1:moveto(arg2, arg3, arg4, arg5)
    end
end
Actor.moveto = function(arg1, arg2, arg3, arg4, arg5) -- line 455
    if type(arg2) == "table" then
        PutActorAt(arg1.hActor, arg2.use_pnt_x, arg2.use_pnt_y, arg2.use_pnt_z, arg5)
    else
        PutActorAt(arg1.hActor, arg2, arg3, arg4, arg5)
    end
end
Actor.driveto = nil
Actor.teleport_out_of_hot_box = function() -- line 463
end
Dialog.mouseSelect = function(arg1, arg2, arg3) -- line 465
    arg1.selected_line = arg2
    arg1:update_colors()
    if arg3 == 1 and arg2 > 0 and arg2 < arg1.next_line then
        start_script(arg1.execute_line, arg1, arg1.selected_line)
    end
end
curbman = function() -- line 494
end
input_boot_parameter = function() -- line 496
    local local1
    local1 = InputDialog("Boot Parameter", "Enter jump number:")
    start_script(jump_script2, local1)
end
jump_script2 = function(arg1) -- line 501
    if arg1 == "cs1" then
        ga.work_order:get()
        co.computer.set_to_sign = TRUE
    elseif arg1 == "rf" then
        fe.basket.pickUp()
    elseif arg1 == "al" then
        reaped_meche = TRUE
        al:switch_to_set()
        al:enter()
    elseif arg1 == "bd" then
        bd.extinguisher:get()
        bd.entered_bd = TRUE
        bd:switch_to_set()
    elseif arg1 == "si" then
        si.naranja_out = TRUE
        si:switch_to_set()
        manny:put_in_set(si)
    elseif arg1 == "gh2" then
        glottis.ripped_heart = TRUE
        glottis.heartless = FALSE
        mod_solved = TRUE
        sg:switch_to_set()
        start_script(sg.replace_heart, sg)
    elseif arg1 == "tr" then
        glottis.ripped_heart = TRUE
        glottis.heartless = FALSE
        sg:switch_to_set()
        start_script(tr.drive_in, tr)
    elseif arg1 == "na" then
        nav_solved = TRUE
        na:switch_to_set()
    elseif arg1 == "vd" then
        vd.door_busted = TRUE
        meche.locked_up = TRUE
        vd.door_open = TRUE
        vd:switch_to_set()
    elseif arg1 == "me" then
        me:switch_to_set()
        me:setup_part2()
    elseif arg1 == "ly" then
        fi.gun:get()
        manny.fancy = TRUE
        ly:switch_to_set()
        ly.brennis_obj:use()
    elseif arg1 == "zw" then
        manny.been_in_at = TRUE
        zw:switch_to_set()
        start_script(cut_scene.albinizod)
    elseif arg1 == "sh" then
        bowlsley_in_hiding = TRUE
        th.grinder.has_bone = TRUE
        th.grinder:get()
        sh:switch_to_set()
    else
        jump_script(arg1)
    end
end
START_CUT_SCENE = function(arg1) -- line 559
    PrintDebug("start_cut_scene")
    InteractMode(1)
    if cutSceneLevel == 0 then
        cameraman_disabled = TRUE
    end
    cutSceneLevel = cutSceneLevel + 1
    stop_movement_scripts()
    if arg1 == "no head" then
        enable_head_control(FALSE)
    end
end
END_CUT_SCENE = function() -- line 571
    if cutSceneLevel > 0 then
        PrintDebug("end_cut_scene")
        cutSceneLevel = cutSceneLevel - 1
        if cutSceneLevel == 0 then
            InteractMode(0)
            cutSceneLevel = 0
            cameraman_disabled = FALSE
            set_override(nil)
            ResetMarioControls()
            single_start_script(WalkManny)
            time_to_look = TRUE
            start_script(check_for_movement_keys)
        end
    end
end
trim_header = function(arg1) -- line 587
    local local1, local2, local3
    if not arg1 then
        return "", ""
    end
    if strsub(arg1, 1, 1) == "/" then
        local3 = strfind(arg1, "/", 2, TRUE)
        if local3 then
            local1 = strsub(arg1, local3 + 1)
            local2 = strsub(arg1, 1, local3)
        else
            local1 = strsub(arg1, 10, strlen(arg1))
            local2 = strsub(arg1, 1, 9)
        end
        arg1 = local1
    end
    return arg1, local2
end
if not al.dummy_door then
    al.dummy_door = Object:create(al, "/altxa00/dummydoor", 0, 100, 0, { range = 0.100000001 })
    al.dummy_door:make_untouchable()
end
pc_rename(al.ga_door_obj, "/altxa01/big door")
at.ledge.use_immediate = TRUE
bd.extinguisher.use_immediate = TRUE
-- (PointyClicky Edition, docs/moments.md line 16: the extinguisher is the game's
-- own bd.extinguisher.use again, held U to spray, let go to stop; the engine holds
-- U for as long as the finger is down. Grim Mouse's tap-to-toggle is retired.)
pc_rename(bv.bone_wagon, "/bvtxa00/bonewagon")
pc_rename(bv.padlock, "/bvtx043/padlock")
pc_rename(bv.padlock_obj, "/bvtxa01/padlock")
pc_rename(bv.gate, "/bvtx053/gate")
pc_rename(bv.bd_door, "/bvtxa02/door")
pc_rename(cf.panel, "/cftxa00/panel")
pc_rename(cf.panelcu, "/cftxa01/panel")
pc_rename(cf.drawer, "/cftxa02/drawer")
pc_rename(cf.lounge, "/cftxa03/lounge")
pc_rename(cn.charlie_obj, "/cntxa06/charlie")
pc_rename(cn.printer, "/cntxa05/printer")
pc_rename(cn.ticket, "/cntxa04/stub")
pc_rename(cn.bogen_obj, "/cntxa00/bogen")
pc_rename(cn.gamblers, "/cntxa01/gamblers")
pc_rename(cn.croupier_obj, "/cntxa02/croupier")
pc_rename(cn.pass, "/cntxa03/pass")
-- PointyClicky Edition (15 Nov 2026), Grim Mouse's crash at the computer
-- (its issue #48, "Domino's" computer: Copal's, Year 1). A hover queues
-- draw_choices; the click's make_selection runs ahead of it and, when the
-- reply doesn't change, stop_interface purges the screen's primitives in the
-- same frame, so the queued draw_choices hits a purged one (ChangePrimitive
-- asserts). stop_interface clears interface_active first: after that a
-- leftover draw_choices has nothing to draw, and a late pointer event nothing to do.
if not pc_co_draw_choices then
    pc_co_draw_choices = co.computer.draw_choices
end
co.computer.draw_choices = function(arg1)
    if co.computer.interface_active then
        pc_co_draw_choices(arg1)
    end
end
-- PointyClicky Edition (proof playthrough, 15 Nov 2026): co.lua's patch puts the
-- pointer in its dialogue mode when the computer opens, and only Grim Mouse's
-- mouseSelect put it back. The computer is worked by its own keys now
-- (docs/moments.md line 11), so after a reply (or Esc) every tap went on to the
-- closed computer and Manny was stuck in Copal's office. Leaving the computer
-- puts the pointer back, whichever way it's left.
if not pc_co_stop_interface then
    pc_co_stop_interface = co.computer.stop_interface
end
co.computer.stop_interface = function(arg1)
    SwitchControlMode(0)
    pc_co_stop_interface(arg1)
end
-- (and a save made while stuck so comes back with the pointer free: this file
-- runs again after every load)
if system.lastDialog == co.computer and not co.computer.interface_active then
    system.lastDialog = nil
    SwitchControlMode(0)
end
co.computer.mouseSelect = function(arg1, arg2, arg3) -- line 753
    if not co.computer.interface_active then
        return
    end
    if arg2 > 0 and co.computer.selection ~= arg2 - 1 then
        start_sfx("cpuBeep2.WAV")
    end
    if arg2 == 0 then
        co.computer.selection = 0
    else
        co.computer.selection = arg2 - 1
    end
    if arg3 == 0 then
        start_script(co.computer.draw_choices, co.computer)
    end
    if arg3 == 1 and arg2 > 0 then
        SwitchControlMode(0)
        start_script(co.computer.make_selection, co.computer)
    elseif arg3 == 2 and arg2 > 0 then
        start_script(co.computer.select_response, co.computer)
    end
end
if not cy.offbelt then
    cy.offbelt = Object:create(cy, "/cytxa00/offbelt", 100, 0, 0, { range = 0.100000001 })
end
cy.offbelt.use_pnt_x = 0.0754809976
cy.offbelt.use_pnt_y = 3.71420002
cy.offbelt.use_pnt_z = 0.115829997
cy.offbelt.use = function(arg1) -- line 776
    start_script(cy.jump_off_conveyor, cy)
end
pc_rename(dd.terry_obj, "/ddtxa00/terry")
pc_rename(dp.anchor, "/dptxa00/anchor")
pc_rename(ei.dp_button, "/eitxa00/button")
pc_rename(ei.op_button, "/eitxa01/button")
pc_rename(ei.intruments, "/eitxa02/instruments")
pc_rename(ei.left_control, "/eitxa03/lever")
pc_rename(ei.right_control, "/eitxa04/lever")
pc_rename(ei.engine, "/eitxa05/engine")
pc_rename(ei.spot, "/eitxa06/spot")
pc_rename(ei.glottis_obj, "/eitxa07/Glottis")
pc_rename(ei.op_door, "/eitxa07/door")
pc_rename(ei.il_door, "/eitxa08/hatch")
gs.ga_door.comeOut = function(arg1) -- line 923
end
pc_rename(hl.raoul_obj, "/hltxa00/Raoul")
pc_rename(il.corpse1, "/iltxa00/body")
pc_rename(il.corpse2, "/iltxa01/body")
pc_rename(il.corpse3, "/iltxa02/bodies")
pc_rename(il.corpse4, "/iltxa03/bodies")
pc_rename(il.ladder, "/iltxa05/ladder")
pc_rename(il.lz_door, "/iltxa04/hatch")
pc_rename(lz.port_pipe, "/lztxa00/vent")
pc_rename(lz.starboard_pipe1, "/lztxa01/vent")
pc_rename(lz.starboard_pipe2, "/lztxa02/vent")
pc_rename(lz.cleat1, "/lztxa03/cleat")
pc_rename(lz.cleat2, "/lztxa04/cleat")
pc_rename(lz.il_door, "/lztxa05/door")
pc_rename(me.ticket, "/metxa21/Double-N ticket")
pc_rename(me.door_flowers, "/metxa22/flowers")
pc_rename(me.darts, "/metxa23/darts")
pc_rename(me.salvador_obj, "/metxa20/Salvador's head")
if not me.salvador2 then
    me.salvador2 = Object:create(me, "/metxa30/Salvador's head", 16.7999992, -19.8999996, -7.85500002, { range = 0.899999976 })
    me.salvador2:make_untouchable()
end
me.salvador2.use_pnt_x = 16.7999992
me.salvador2.use_pnt_y = -19.8999996
me.salvador2.use_pnt_z = -7.85500002
me.salvador2.lookAt = function(arg1) -- line 956
    me.salvador_obj:lookAt()
end
me.salvador2.use = function(arg1) -- line 959
    me.salvador_obj:pickUp()
end
me.salvador_obj.use_immediate = TRUE
me.ticket.inv_name = "tix"
mf.wound.use_immediate = TRUE
-- (Grim Mouse makes the wound touchable for good; mf.lua never takes it back,
-- so doing it again after a load changes nothing)
if not mf.wound.touchable then
    mf.wound:make_touchable()
end
pc_rename(nq.meche_obj, "/nqtxa10/Meche")
nq.inv_name = "lsa_photo"
pc_rename(op.anchor, "/optxa00/anchor")
pc_rename(op.ei_door, "/optxa01/door")

ri.photo.inv_name = "celso_photo"
pc_rename(sh.glottis_obj, "/shtxa01/glottis")
pc_rename(sh.flower_trail_obj, "/shtxa02/master flower trail")
pc_rename(sh.te_ladder, "/shtx010/ladder")
sh.remote.use_immediate = TRUE
si.photofinish.use_immediate = TRUE
sl.key.inv_name = "old_key"
sl.key.use_on_door = TRUE
st.rp_door.out_rot_y = 0
su.moving_chepito_obj.use_pnt_x = 0.251300007
su.moving_chepito_obj.use_pnt_y = -4.1566
su.moving_chepito_obj.use_pnt_z = 0


su.mouseSpecial = function(arg1, arg2, arg3) -- line 1025
    if arg3 > 0 then
        if arg2 == "/dxlantern" then
            Dialog:clear()
            Dialog:finish()
            SwitchControlMode(2)
            start_script(su.grab_lantern)
        elseif arg2 == "/dxglottis" then
            start_script(su.give_chepito_to_glottis)
        end
    end
end
su.stop_chepito = function(arg1) -- line 1037
    if proximity(manny, chepito) < 3 then
        START_CUT_SCENE("no head")
        SwitchControlMode(10)
        local local1
        local1 = chepito:getpos()
        manny:say_line("/suma141/")
        stop_script(su.chepito_orbit)
        chepito:stop_walk()
        chepito:walkto(0.699999988, -4, 0)
        chepito:wait_for_actor()
        local1 = chepito:getpos()
        while TurnActorTo(manny.hActor, local1.x, local1.y, local1.z) do
        end
        END_CUT_SCENE()
        Dialog:run("cp1", "dlg_chepito.lua")
    else
        manny:say_line("/suma141/")
        wait_for_message()
        manny:say_line("/suma142/")
    end
end
tg.note.inv_name = "gk_note"
ts.tx_door.walkOut = function(arg1) -- line 1130
    tx:come_out_door(tx.ts_door)
end
pc_rename(tu.extinguisher, "/tutx018/fire extinguisher")
if not tu.red_tube_os then
    tu.red_tube_os = Object:create(tu, "/tutxc01/red tube", 0.647489011, -0.162466004, 0.360000014, { range = 9.99999994e-09 })
end
tu.red_tube_os.use_pnt_x = 1.15021002
tu.red_tube_os.use_pnt_y = -0.162992999
tu.red_tube_os.use_pnt_z = 0
tu.red_tube_os.use_rot_x = 0
tu.red_tube_os.use_rot_y = 4.28539991
tu.red_tube_os.use_rot_z = 0
tu.red_tube_os.lookAt = function(arg1) -- line 1141
    tu.red_tube:lookAt()
end
tu.red_tube_os.use = function(arg1) -- line 1144
    system.default_response("reach")
end
pc_rename(vi.broadaxe, "/vitxa04/axe")
if not vo.dummy_axe then
    vo.dummy_axe = Object:create(vo, "/votxb00/broadaxe", 0, 100, 0, { range = 0 })
end
vo.dummy_axe.use_immediate = TRUE
vo.dummy_axe.use = function(arg1) -- line 1161
    single_start_script(vo.drop_axe, vo)
end
-- PointyClicky Edition (14 Nov 2026): Manny finds, the cursor confirms.
-- Every frame the game's own Head_Control picks hot_object, the thing
-- Manny's head turns to (_system.lua: within reach, nearest in angle). Each
-- one he turns to is noticed, for good in this playthrough (the engine keeps
-- it in the save), and only noticed things light the cursor.
-- (Taken once: run again, after a load, this must not wrap itself.)
if not pc_Head_Control then
    pc_Head_Control = Head_Control
end
Head_Control = function()
    pc_Head_Control()
    if hot_object and hot_object.hotspot_id then
        NoticeHotspot(hot_object.hotspot_id)
    end
end
-- PointyClicky Edition (14 Nov 2026): the inventory is Manny's own coat, the
-- 1998 close-up (Simon: "the coat, 100%"), never Grim Mouse's grid. Grim
-- Mouse's patched _inventory.lua opens and closes the inventory through these
-- three; pointing them back at the game's own coat routines brings the coat
-- back, and keeps every fix that patch carries. The original's keys drive it
-- (the arrows, U, E, Esc): the engine turns taps into them (HotspotMan).
suitInventoryButtonHandler2 = suitInventoryButtonHandler
Inventory.setup_draw = function(arg1)
    Inventory:switch_to_set()
end
Inventory.unload_inventory = function(arg1)
    mannys_hands:wait_for_chore()
    Inventory:return_to_set()
    inventory_save_set:current_setup(inventory_save_setup)
    manny:setpos(inventory_save_pos)
end
-- (after a load: the links aren't in the save; the current set's again)
if system.currentSet then
    pc_link_actors(system.currentSet)
end
-- PointyClicky Edition (15 Nov 2026, the proof playthrough): the wheelbarrow and
-- the anchor room crawl are the 1998 loops again (tr.lua and ac.lua's patches:
-- Grim Mouse had made them run on while its linear-mode script ran, and with
-- that script retired find_script(nil) kept them running, so a pull never ended
-- and Manny pushed the barrow off down the road). A save made before this
-- carries the old loops; for those, the names they ask about stand for a script
-- that never runs, so find_script answers nil as the 1998 loops' keys do.
pc_never_runs = function() end
if tr and not tr.linearMovePlus then
    tr.linearMovePlus = pc_never_runs
    tr.linearMoveMinus = pc_never_runs
end
if ac and not ac.linearMovePlus then
    ac.linearMovePlus = pc_never_runs
    ac.linearMoveMinus = pc_never_runs
end
