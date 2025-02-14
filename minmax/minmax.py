from abc import ABC, abstractmethod
from enum import Enum


# Assumptions:
#   1) For any two nodes A -> B connected by a single move, there is only one action that will move from A to B

class PlayerType(Enum):
    # Player type
    USER = 0
    AI = 1


# Min-max tree which defines search parameters and information about the game
class MinMaxTree:
    def __init__(self, players=None):
        # Initializes the tree
        # players   - A dictionary of players with the value being a PlayerType
        if players is None:
            self.__players = {}
        else:
            self.__players = players.copy()
        self._nodes = {}

    # Properties
    @property
    def players( self ):
        return self.__players

    @players.setter
    def players( self, players ):
        self.__players = players.copy()

        for node in self._nodes:
            node.update_players()

    def is_player( self, player ):
        return player in self.__players.keys()

    @property
    def num_players( self ):
        return len( self.__players.keys() )

    @property
    def nodes( self ):
        return self._nodes.copy()

    # Node functions
    def add_node( self, node ):
        if node is not None:
            self._nodes[node.id] = node

    def get_node( self, id ):
        return self._nodes[id]

    def remove_node( self, id ):
        return self._nodes.pop( id, None )

    def update_node_id( self, old_id ):
        node = self.remove_node( old_id )
        self.add_node( node )

    def update_nodes( self ):
        for node in self._nodes:
            node.update()


class Node(ABC):

    # Initialization
    def __init__(self, min_max_tree):
        self._tree = min_max_tree
        self.__id = None
        self._expanded = False
        self._values = {}
        self.transitions = []
        self.__best_moves = {}

        # Initialize id
        self.init_id()
        self.update_players()

    @abstractmethod
    def init_id( self ):
        # Initializes the id property which adds the Node to the MinMaxTree
        # self.id = new_id should be called in this function
        raise NotImplementedError

    # Properties
    @property
    def id( self ):
        return self.__id

    @id.setter
    def id( self, id ):
        # Sets the Node ID and updates the MinMaxTree
        # For efficiency it is recommended this property be set once and not change
        old_id = self.__id
        self.__id = id
        if old_id is None:
            self._tree.add_node( self )
        else:
            self._tree.update_node_id( old_id )

    @property
    def values( self ):
        return self._values.copy()

    def value( self, player ):
        return self._values[player]

    def best_move( self, player ):
        return self.__best_moves[player].action

    # Transition functions
    def add_transition( self, transition ):
        self.transitions.append( transition )

    def remove_transition( self, transition ):
        self.transitions.remove( transition )

    # Expansion functions
    @abstractmethod
    def expand(self, depth=-1):
        # Expands the node by generating transitions and children nodes
        # When this function is called, the self._expanded property should be set True
        raise NotImplementedError

    @property
    def expanded( self ):
        return self._expanded

    @property
    @abstractmethod
    def terminal( self ):
        # Returns T/F if this node is a terminal node with no children
        raise NotImplementedError

    # Update process
    def update( self ):
        # Updates the value of this node based on its state and children
        # This function has been stripped to only the necessary calculations needed each time
        # The node will be updated with the optimal move for each AI player.
        # The optimal move will not be calculated for players with the USER type
        # It is left to the user to ensure all nodes have their properties updated correctly
        # Functions to ensure are called before updating
        #   - update_players()
        # Functions called during the update process
        #   - update_values()
        if not self._expanded or self.terminal:
            self.update_values()
        else:
            # Reset best moves
            for key in self.__best_moves.keys():
                self.__best_moves[key] = None
                self._values[key] = None

            # Search through children for the best move for each AI player
            for transition in self.transitions:
                end_value = transition.end_node.value( transition.next_player )
                if self._values[transition.current_player] is None or -end_value > self._values[transition.current_player]:
                    self._values[transition.current_player] = -end_value
                    self.__best_moves[transition.current_player] = transition

    def update_players( self ):
        # Updates the number of players from the MinMaxTree.
        # If the number of players has changed, all values will be set to zero
        if self._tree.num_players != len( self._values.keys() ):
            self._values.clear()
            self.__best_moves.clear()
            for key in self._tree.players.keys():
                self._values[key] = 0
                self.__best_moves[key] = None

    @abstractmethod
    def update_values( self ):
        # Updates the values of each AI player for use in the min-max algorithm
        # It is assumed each player desires a higher value and the highest value child will be taken as the optimal move
        # This method will only be called if it is the last node in a branch. The last node could either be a terminal
        # node or the last node at the current search depth. This function should handle both cases
        # This function should set each key's value in self._values
        raise NotImplementedError

    # Comparison functions
    def __eq__( self, node ):
        if isinstance( node, Node ):
            return self.id == node.id
        else:
            return super().__eq__( node )


class Transition:

    def __init__( self, start_node, end_node, current_player, next_player, action ):
        self.__start_node = None
        self.__end_node = None
        self.__current_player = None
        self.__next_player = None
        self.__action = None

        self.start_node = start_node
        self.end_node = end_node
        self.current_player = current_player
        self.next_player = next_player
        self.action = action

    @property
    def start_node( self ):
        return self.__start_node

    @start_node.setter
    def start_node( self, start_node ):
        if not isinstance( start_node, Node ):
            raise TypeError
        self.__start_node = start_node

    @property
    def end_node( self ):
        return self.__end_node

    @end_node.setter
    def end_node( self, end_node ):
        if not isinstance( end_node, Node ):
            raise TypeError
        self.__end_node = end_node

    @property
    def current_player( self ):
        return self.__current_player

    @current_player.setter
    def current_player( self, current_player ):
        self.__current_player = current_player

    @property
    def next_player( self ):
        return self.__next_player

    @next_player.setter
    def next_player( self, next_player ):
        self.__next_player = next_player

    @property
    def action( self ):
        return self.__action

    @action.setter
    def action( self, action ):
        self.__action = action

