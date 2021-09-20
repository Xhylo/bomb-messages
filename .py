    #################
    # bomb_messages #
    #################
    elif command == 'bomb_messages' or command == 'bomb_message' or command == 'bomb':
        if args is None:
            status_list = []
            features_list = []
            
            features_list.append('random')
            if settings['bomb_messages']['random'] is None:
                status_list.append(':x:')
            else:
                status_list.append(':white_check_mark:')

            features_list.append('fixed')
            if len(settings['bomb_messages']['fixed']) == 0:
                status_list.append(':x:')
            else:
                status_list.append(':white_check_mark:')

            theColor = randint(0, 0xFFFFFF)
            embed = discord.Embed(
                title = 'bomb_messages',
                description = f'Config for all the bomb commands.\nWhen you run bomb commands like `{settings["command_prefix"]}channelbomb 100 fixed` the fixed is the type of word list you are going to use. In this case the word list is going to randomly pick texts from the "fixed" list.\n\n:white_check_mark: = Ready to use\n:x: = Needs to config\ncolor: #{hex(theColor)[2:].zfill(6)}',
                color = theColor
            )
            embed.add_field(name='Status', value='\n'.join(status_list), inline=True)
            embed.add_field(name='Types', value='\n'.join(features_list), inline=True)
            embed.add_field(name='Usage', value=f'`bomb_messages fixed add <command>` - add contents to the back of the list\n\n`bomb_messages fixed remove <line number> [line number] [line...` - remove line(s) from the list\n\n`bomb_messages fixed list [page number]` - list contents that are in the content list\n\n`bomb_messages random <character length>` - sets character length for bomb commands like `{settings["command_prefix"]}kaboom 100 b64`(b64 = base64) ', inline=False)

            embed.set_footer(text='Config is saved' if configIsSaved() else '(*)Config is not saved')
            await ctx.send(embed=embed)

        else:
            args = args.split()
            if args[0].lower() == 'random':
                if len(args) > 1 and args[1].isdigit() and (1 <= (length := int(args[1])) <= 1024):
                    settings['bomb_messages']['random'] = length
                    await log(ctx, f'Random-message length has been set to `{str(length)}`.')
                else:
                    await log(ctx, 'Please enter a positive integer that is between 1 and 1024.')

            elif args[0].lower() == 'fixed':
                if args[1] == 'add':
                    if len(args) > 2 and (1 <= len(text := ' '.join(args[2:])) <= 100):
                        settings['bomb_messages']['fixed'].append(text)
                        await log(ctx, f'Text added. Character length: `{str(len(text))}`.')
                    else: 
                        await log(ctx, f'Please enter something that has 1 to 100 characters.')

                elif args[1] == 'remove':
                    if len(args) > 2:
                        del args[0], args[0]
                        offset = 1
                        initial_length = len(settings['bomb_messages']['fixed'])
                        for item in args:
                            if item.isdigit() and (0 <= (item := int(item)) - offset <= initial_length - offset):
                                del settings['bomb_messages']['fixed'][item - offset]
                                offset += 1
                            else:
                                await log(ctx, f'Skipped deleting line `{item}` -> not an integer between 1 and {str(initial_length)}.')

                        await log(ctx, f'Successfully removed `{str(offset - 1)}` items.')
                    else:
                        await log(ctx, f'Enter line(s) to remove from bomb_messages fixed list.')
                
                elif args[1] == 'list':
                    await embed_list(args[2] if len(args) > 2 else '1', 'bomb_messages fixed list', settings['bomb_messages']['fixed'])

                else:
                    await log(ctx, f'Unknown operation: `{args[1]}`')

            else:
                await log(ctx, f'Unable to find {args[0]} config.')

