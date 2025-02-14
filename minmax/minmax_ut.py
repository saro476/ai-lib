import unittest
from minmax import *


class TestNode( Node ):
    # Dummy implementation of a Node class for testing purposes

    id_counter = 0

    def init_id( self ):
        self.id = TestNode.id_counter
        TestNode.id_counter += 1

    def expand( self, depth = -1 ):
        return

    def terminal( self ):
        return self.id % 2 == 0

    def update_values( self ):
        pass


class MinMaxTest( unittest.TestCase ):
    players = {1:PlayerType.USER, 2:PlayerType.AI}
    tree = MinMaxTree(players)
    node = TestNode(tree, 1)

    def test_MinMaxTree( self ):
        # Test constructor
        tree2 = MinMaxTree( {1:PlayerType.USER, 2:PlayerType.AI, 3:PlayerType.USER} )
        self.assertEqual(self.tree.num_players, 2)
        self.assertEqual(tree2.num_players, 3)

    def test_Node( self ):
        # Test constructor
        node2 = TestNode(self.tree, 2)

        self.assertEqual( len(self.tree.nodes), 2)

        # Test id getter
        self.assertEqual(self.node.id, 0)

        # Test id setter
        self.node.id = 100
        node2.id = 200
        self.assertEqual(self.node.id, 100)
        self.assertEqual(node2.id, 200)


if __name__ == '__main__':
    unittest.main()
