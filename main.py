import random
import os
import math

money = 500
dealer_cards = []
player_cards = []


class Deck(object):
  def __init__(self):
    self.current_deck = []
    self.shuffle()
    
  def __get_card_ind(self) -> int:
    if len(self.current_deck) <= 3:
      raise ValueError("DECK NEEDS SHUFFLED")
    return random.randint(0, len(self.current_deck) - 1)
    
  def deal(self) -> [list, list]:
    cards = []
    
    for i in range(4):
      index = self.__get_card_ind()
      cards.append(self.current_deck[index])
      self.current_deck.pop(index)
      
    return [cards[0], cards[1]], [cards[2], cards[3]]
    
  def get_card(self):
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
  
deck = Deck()

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


while money != 0:
  player_bust = False
  dealer_bust = False
  player_blackjack = False
  dealer_blackjack = False
  hit = True
  first_turn = True
  
  while True:
    print(f"Money: ${money}")
    bet = input(f"Bet: ")
    try:
      bet = int(bet)
    except ValueError:
      continue
      
    break
      
  deck.shuffle() #shuffle every hand
  player_cards, dealer_cards = deck.deal()
  player_value = 0
  dealer_value = 0

  #Hitting Phase
  while True:
    os.system('clear')
    dealer_cards_visible = ['?', *dealer_cards[1:]]

    player_value = get_value(player_cards)
    print(f"Your Cards: {player_cards}")
    print(f"Dealer's Cards: {dealer_cards_visible}")
    
    if player_value == 21 and first_turn:
      player_blackjack = True
      break
    elif player_value == 21:
      break
    elif player_value > 21:
      print("You went bust")
      player_bust = True
      break
      
    
    choice = 0

   #ADD SPLIT LATER
    if first_turn and money >= bet * 2: #can double down
      choice = input("Hit(0), Stand(1), Double Down(2): ")
    else:
      choice = input("Hit(0), Stand(1): ")

    try:
      choice = int(choice)
    except ValueError:
      print("INVALID VALUE :: STANDING")
      choice = 1

    first_turn = False
    if choice == 2:
      player_cards.append(deck.get_card())
      break
    elif choice == 0:
      player_cards.append(deck.get_card())
    else:
      break
  
  #Player Went Bust
  if player_bust:
    os.system('clear')
    print(f"Your Cards: {player_cards}")
    print(f"Dealer's Cards: {dealer_cards}")
    money -= bet
    continue
  elif player_blackjack:
    os.system('clear')
    print(f"Your Cards: {player_cards}")
    print(f"Dealer's Cards: {dealer_cards}")
    print("BlackJack!")
    money += math.ceil(bet * 1.5)
    continue
  
  #Dealer Phase
  while True:
    dealer_value = get_value(dealer_cards)
    
    if dealer_value > 21:
      dealer_bust = True
      break
    elif dealer_value >= 17:
      break
    
    dealer_cards.append(deck.get_card())
    
  
  os.system('clear')
  print(f"Your Cards: {player_cards}")
  print(f"Dealer's Cards: {dealer_cards}")
  
  
  #Final Checks
  if (dealer_bust):
    print("Dealer went bust")
    money += bet
    continue
  elif (player_value == dealer_value):
    print("It's a push")
    continue
  elif (player_value > dealer_value):
    print("You win!")
    money += bet
    continue
  else:
    print("You lost!")
    money -= bet
    continue
