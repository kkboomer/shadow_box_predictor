import predictor
import pygame

def main():
    pygame.init()
    screen = pygame.display.set_mode((1000, 800))
    pygame.display.set_caption("Shadow Boxing Predictor - Turn Based")
    
    large_font = pygame.font.SysFont("Inter", 52, bold=True)
    medium_font = pygame.font.SysFont("Inter", 32)
    small_font = pygame.font.SysFont("Inter", 22)
    
    p1 = predictor.Predictor()
    p2 = predictor.Predictor()
    
    p1_keys = {pygame.K_w: "UP", pygame.K_s: "DOWN", pygame.K_a: "LEFT", pygame.K_d: "RIGHT"}
    p2_keys = {pygame.K_UP: "UP", pygame.K_DOWN: "DOWN", pygame.K_LEFT: "LEFT", pygame.K_RIGHT: "RIGHT"}
    sequence_enter = pygame.K_RETURN
    
    # --- TURN & ROLE STATE ---
    current_attacker = "P1"  # "P1" or "P2"
    p1_score = 0
    p2_score = 0
    round_result_text = "Press WASD / Arrows, then ENTER to finish turn"
    
    # Prediction state
    p1_pred, p1_conf, p1_model = "WAITING...", 0.0, "None"
    p2_pred, p2_conf, p2_model = "WAITING...", 0.0, "None"
    
    running = True
    while running:
        screen.fill((25, 30, 45)) # Dark slate background
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                
            elif event.type == pygame.KEYDOWN:
                if event.key in p1_keys:
                    p1.update_history(p1_keys[event.key])
                    
                elif event.key in p2_keys:
                    p2.update_history(p2_keys[event.key])
                    
                elif event.key == sequence_enter:
                    # Make sure both players submitted a move for this round
                    if len(p1.history) > 0 and len(p2.history) > 0:
                        last_p1_move = p1.history[-1]
                        last_p2_move = p2.history[-1]
                        
                        # --- GAME RULES & ROLE SWAPPING LOGIC ---
                        if last_p1_move == last_p2_move:
                            # Attacker landed a point!
                            if current_attacker == "P1":
                                p1_score += 1
                                round_result_text = "P1 HIT! P1 stays Attacker."
                            else:
                                p2_score += 1
                                round_result_text = "P2 HIT! P2 stays Attacker."
                        else:
                            # Defender dodged! Roles swap.
                            if current_attacker == "P1":
                                current_attacker = "P2"
                                round_result_text = "P1 MISSED! P2 is now ATTACKING."
                            else:
                                current_attacker = "P1"
                                round_result_text = "P2 MISSED! P1 is now ATTACKING."

                        # Generate predictions for the NEXT turn
                        p1_pred, p1_conf, p1_model = p1.predict_next_move()
                        p2_pred, p2_conf, p2_model = p2.predict_next_move()

        # ==========================================
        # DYNAMIC UI RENDERING
        # ==========================================
        
        # 1. TOP STATUS BAR: Current Roles & Scores
        score_txt = medium_font.render(f"P1 Score: {p1_score}  |  P2 Score: {p2_score}", True, 'white')
        screen.blit(score_txt, (screen.get_width() // 2 - score_txt.get_width() // 2, 20))
        
        result_txt = small_font.render(round_result_text, True, (200, 220, 255))
        screen.blit(result_txt, (screen.get_width() // 2 - result_txt.get_width() // 2, 65))

        # 2. DYNAMIC CENTER HUD (Focuses on the Attacker's predicted target)
        if current_attacker == "P1":
            target_pred, target_conf = p1_pred, p1_conf
            hud_title = "P1 IS ATTACKING → Predict P1's Target:"
            hud_color = (100, 180, 255) # P1 Blue
        else:
            target_pred, target_conf = p2_pred, p2_conf
            hud_title = "P2 IS ATTACKING → Predict P2's Target:"
            hud_color = (255, 100, 100) # P2 Red

        hud_header = medium_font.render(hud_title, True, hud_color)
        screen.blit(hud_header, (screen.get_width() // 2 - hud_header.get_width() // 2, 120))
        
        pred_main = large_font.render(f"{target_pred} ({target_conf:.0%})", True, 'yellow')
        screen.blit(pred_main, (screen.get_width() // 2 - pred_main.get_width() // 2, 165))

        # Debug Model string
        debug_text = small_font.render(f"Models - P1: {p1_model} | P2: {p2_model}", True, (150, 150, 150))
        screen.blit(debug_text, (screen.get_width() // 2 - debug_text.get_width() // 2, 225))

        # 3. PLAYER 1 PANEL (Left)
        p1_role = "[ATTACKER]" if current_attacker == "P1" else "[DEFENDER]"
        p1_color = (100, 180, 255) if current_attacker == "P1" else (120, 120, 120)
        
        screen.blit(medium_font.render(f"P1 (WASD) {p1_role}", True, p1_color), (80, 280))
        screen.blit(small_font.render(f"Next Predicted: {p1_pred}", True, 'white'), (80, 320))
        screen.blit(small_font.render("History:", True, (200, 200, 200)), (80, 360))
        for i, move in enumerate(p1.history[-10:]):
            txt = small_font.render(move, True, p1_color)
            screen.blit(txt, (80, 390 + (i * 25)))

        # 4. PLAYER 2 PANEL (Right)
        p2_role = "[ATTACKER]" if current_attacker == "P2" else "[DEFENDER]"
        p2_color = (255, 100, 100) if current_attacker == "P2" else (120, 120, 120)
        
        screen.blit(medium_font.render(f"P2 (Arrows) {p2_role}", True, p2_color), (650, 280))
        screen.blit(small_font.render(f"Next Predicted: {p2_pred}", True, 'white'), (650, 320))
        screen.blit(small_font.render("History:", True, (200, 200, 200)), (650, 360))
        for i, move in enumerate(p2.history[-10:]):
            txt = small_font.render(move, True, p2_color)
            screen.blit(txt, (650, 390 + (i * 25)))

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()