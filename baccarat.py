import pygame
import random

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Baccarat Game")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 128, 0)
BUTTON_COLOR = (0, 0, 255)
HOVER_COLOR = (0, 0, 200)

suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
values = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 0, 'J': 0, 'Q': 0, 'K': 0, 'A': 1}

class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
        self.value = values[rank]

    def __repr__(self):
        return f"{self.rank} of {self.suit}"

def create_deck(num_decks=6):
    deck = []
    for _ in range(num_decks):
        for suit in suits:
            for rank in ranks:
                deck.append(Card(suit, rank))
    random.shuffle(deck)
    return deck

def calculate_hand(hand):
    total = sum(card.value for card in hand) % 10
    return total

class Button:
    def __init__(self, x, y, width, height, text, action=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.action = action
        self.font = pygame.font.Font(None, 36)
        self.default_color = BUTTON_COLOR
        self.hover_color = HOVER_COLOR

    def draw(self, screen):
        color = self.hover_color if self.is_hovered() else self.default_color
        pygame.draw.rect(screen, color, self.rect)
        text_surface = self.font.render(self.text, True, WHITE)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def is_hovered(self):
        mouse_pos = pygame.mouse.get_pos()
        return self.rect.collidepoint(mouse_pos)

    def click(self):
        if self.is_hovered() and self.action:
            self.action()

def game_loop():
    global deck, player_hand, banker_hand, winner, player_card_index, banker_card_index
    clock = pygame.time.Clock()
    running = True
    winner = None

    if not deck:
        deck = create_deck()

    deal_button = Button(WIDTH // 2 - 100, HEIGHT - 150, 200, 50, "Deal Cards", deal_card)
    reset_button = Button(WIDTH // 2 - 100, HEIGHT - 75, 200, 50, "Reset Game", reset_game)

    while running:
        screen.fill(GREEN)

        if len(player_hand) < 2 or len(banker_hand) < 2:
            deal_button.draw(screen)
            reset_button.draw(screen)
        else:
            player_score = calculate_hand(player_hand)
            banker_score = calculate_hand(banker_hand)

            if player_score > banker_score:
                winner = "Player Wins!"
            elif banker_score > player_score:
                winner = "Banker Wins!"
            else:
                winner = "It's a Tie!"

            font = pygame.font.Font(None, 36)
            text = font.render(f"Player Hand: {player_hand[0]} {player_hand[1]} | Score: {player_score}", True, WHITE)
            screen.blit(text, (20, 50))

            text = font.render(f"Banker Hand: {banker_hand[0]} {banker_hand[1]} | Score: {banker_score}", True, WHITE)
            screen.blit(text, (20, 150))

            text = font.render(winner, True, WHITE)
            screen.blit(text, (WIDTH // 2 - 100, HEIGHT // 2))            
            reset_button.draw(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                deal_button.click()
                reset_button.click()

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

def deal_card():
    global player_hand, banker_hand, winner, deck
    if len(player_hand) < 2:  
        player_hand.append(deck.pop())
    if len(banker_hand) < 2:  
        banker_hand.append(deck.pop())
    
    if len(player_hand) == 2 and len(banker_hand) == 2:
        player_score = calculate_hand(player_hand)
        banker_score = calculate_hand(banker_hand)
        if player_score == banker_score:
            winner = "Tie! Click to deal more cards!"
        else:
            if player_score > banker_score:
                winner = "Player Wins!"
            else:
                winner = "Banker Wins!"
    
def deal_more_cards():
    global player_hand, banker_hand, winner, deck
    if len(player_hand) < 5:
        player_hand.append(deck.pop())
    if len(banker_hand) < 5:
        banker_hand.append(deck.pop())
    
    if len(player_hand) == 5 and len(banker_hand) == 5:
        player_score = calculate_hand(player_hand)
        banker_score = calculate_hand(banker_hand)
        if player_score > banker_score:
            winner = "Player Wins!"
        elif banker_score > player_score:
            winner = "Banker Wins!"
        else:
            winner = "It's a Tie!"
    
def reset_game():
    global player_hand, banker_hand, winner, deck
    player_hand = []
    banker_hand = []
    winner = None
    deck = create_deck()  

deck = []
player_hand = []
banker_hand = []
winner = None

game_loop()
