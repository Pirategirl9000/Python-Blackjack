import random
from os import system as syst
from math import ceil 

money = 500
dealer_cards, player_cards = [], []


class Deck(object):
  def __init__(self) -> None:
    self.current_deck = []
    self.shuffle()
    
  def __get_card_ind(self) -> int:
    if len(self.current_deck) <= 3:
      raise ValueError("DECK NEEDS SHUFFLED")
    return random.randint(0, len(self.current_deck) - 1)
    
  def deal(self) -> tuple[list, list]:
    cards = []
    
    for i in range(4):
      index = self.__get_card_ind()
      cards.append(self.current_deck[index])
      self.current_deck.pop(index)
      
    return [cards[0], cards[1]], [cards[2], cards[3]]
    
  def get_card(self) -> str | int:
    return self.current_deck.pop(self.__get_card_ind())

  def shuffle(self) -> None:
    self.current_deck = [
      'ace', 'ace', 'ace', 'ace',
      2, 2, 2, 2,
      3, 3, 3, 3,
      4, 4, 4, 4,
      5, 5, 5, 5,
      6, 6, 6, 6,
      7, 7, 7, 7,
      8, 8, 8, 8,
      9, 9, 9, 9,
      10, 10, 10, 10,
      'jack', 'jack', 'jack', 'jack',
      'queen', 'queen', 'queen', 'queen',
      'king', 'king', 'king', 'king'
      ] #All 52 cards in a deck
  
def get_value(cards:list) -> int:
  value = 0

  #Get Card Values
  for card in cards:
    if card == 'jack' or card == 'queen' or card == 'king':
      value += 10
    elif card != 'ace':
      value += card
  
  #Ace Check
  for card in cards:
    if card == 'ace':
      if value + 11 > 21:
        value += 1
      else:
        value += 11

  return value


deck = Deck()

while money != 0:
  player_bust = dealer_bust = player_blackjack = dealer_blackjack = False
  player_turn = hit = first_turn = True
  
  while True: #Get bet
    print(f"Money: ${money}")
    bet = input(f"Bet: ")
    try:
      bet = int(bet)
      if (bet > money):
        raise ValueError('Not Enough Money')
    except ValueError:
      continue

    break

  #Game Set-Up
  deck.shuffle() #shuffle every hand
  player_cards, dealer_cards = deck.deal()
  player_value = dealer_value = 0


  #-----------------------------  START OF PLAYERS TURN. -----------------------------#


  while True:
    choice = 0
    dealer_cards_visible = ['?', *dealer_cards[1:]]
    player_value = get_value(player_cards)

    #Checks if the player is bust, blackjack, or 21
    if player_value == 21 and first_turn:
      player_blackjack = True
      break
    elif player_value == 21:
      break
    elif player_value > 21:
      player_bust = True
      break

    if (not player_turn): break

    syst('clear')
    print(f"Your Cards: {player_cards}")
    print(f"Dealer's Cards: {dealer_cards_visible}")
      

    if first_turn and money >= bet * 2:
      choice = input("Hit(1), Stand(2), Double Down(3): ")
    else:
      choice = input("Hit(1), Stand(2): ")

    try: choice = int(choice)
    except ValueError:
      print("INVALID VALUE :: STANDING")
      choice = 1

    first_turn = False

    #Double Down
    if choice == 3:
      player_cards.append(deck.get_card())
      bet *= 2
      player_value = get_value(player_cards)
      player_turn = False
    #Hit
    elif choice == 1: 
      player_cards.append(deck.get_card())
      player_value = get_value(player_cards)
    #Stand
    else:
      player_value = get_value(player_cards)
      player_turn = False


  #-----------------------------  END OF PLAYERS TURN -----------------------------#

  
  if player_bust:
    syst('clear')
    print(f"Your Cards: {player_cards}")
    print(f"Dealer's Cards: {dealer_cards}")
    money -= bet
    print("You went bust!")
    continue
  elif player_blackjack:
    syst('clear')
    print(f"Your Cards: {player_cards}")
    print(f"Dealer's Cards: {dealer_cards}")
    print("BlackJack!")
    money += ceil(bet * 1.5)
    continue
  
  #-----------------------------  START OF DEALERS TURN  -----------------------------#


  while True:
    dealer_value = get_value(dealer_cards)
    
    if dealer_value > 21:
      dealer_bust = True
      break
    elif dealer_value >= 17:
      break
    #Hit
    else:
      dealer_cards.append(deck.get_card())


  #-----------------------------  END OF DEALERS TURN. -----------------------------#
    
  
  syst('clear')
  print(f"Your Cards: {player_cards}")
  print(f"Dealer's Cards: {dealer_cards}")

  #Final Checks
  if (dealer_bust):
    print("Dealer went bust")
    money += bet
  elif (player_value == dealer_value):
    print("It's a push")
  elif (player_value > dealer_value):
    print("You win!")
    money += bet
  else:
    print("You lost!")
    money -= bet