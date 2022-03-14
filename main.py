import sys
import pygame
import GameCls


def main():
    fps = 60
    clock = pygame.time.Clock()
    game = GameCls.Game()
    start = GameCls.Start()
    pause = GameCls.Pause()
    end = GameCls.End()

    # START LOOP ----------------------------------------------------
    start.play_music()
    while True:
        keys = pygame.key.get_pressed()
        game.event()
        start.show_backgroud()
        start.text_draw()

        # GAME LOOP ------------------------------------------------
        if keys[pygame.K_SPACE]:
            start.stop_music()
            game.play_music()
            while game.player.life_func >= 0:
                keys = pygame.key.get_pressed()
                game.event()
                game.backgroung_draw()
                game.text_draw()
                game.player_draw()
                game.cars_draw()
                game.item_draw()
                game.game_logic()
                # PAUSE LOOP -------------------------------------
                if keys[pygame.K_p]:
                    while True:
                        keys = pygame.key.get_pressed()
                        game.event()
                        pause.show_backgroud()
                        pause.text_draw()

                        if keys[pygame.K_ESCAPE]:
                            break

                        pygame.display.update()
                        clock.tick(fps)

                pygame.display.update()
                clock.tick(fps)

            else:
                # END LOOP -------------------------------------

                game.stop_music()
                end.play_music()
                while True:
                    keys = pygame.key.get_pressed()
                    game.event()
                    end.show_backgroud()
                    end.text_draw()

                    if keys[pygame.K_y]:
                        end.stop_music()
                        game.player.reset_car_progress()
                        start.play_music()
                        game.oponents.clear()
                        break

                    if keys[pygame.K_n]:
                        sys.exit()

                    pygame.display.update()
                    clock.tick(fps)

            pygame.display.update()
            clock.tick(fps)

        pygame.display.update()
        clock.tick(fps)


if __name__ == '__main__':
    main()
