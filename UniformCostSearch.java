import search.*;

import java.util.*;

// uniform-cost search

public class Ucs<S, A> {
  public static <S, A> Solution<S, A> search(Problem<S, A> prob) {
    S initState = prob.initialState();
    Set<S> setOfStates = new HashSet<S>();
    Node<S,A> sourceNode = new Node<S,A>(initState);
    sourceNode.setDistance(0);
    sourceNode.setAdjacenciesList(prob.actions(initState));
    sourceNode.setVisited(false);

    PriorityQueue<Node<S,A>> priorityQueue = new PriorityQueue<>();
    priorityQueue.add(sourceNode);
    setOfStates.add(initState);
    Node<S,A> goalNode = null;

    HashMap<S, Node<S,A>> nodes_weights = new HashMap<S, Node<S,A>>();
    nodes_weights.put(initState,sourceNode);

    while( !priorityQueue.isEmpty() ) {
      // Getting the minimum distance Node from priority queue
      Node<S, A> actualNode = priorityQueue.poll();
      actualNode.setAdjacenciesList(prob.actions(actualNode.getName()));

      if(actualNode.isVisited()){
        continue;
      }
      actualNode.setVisited(true);

      if (prob.isGoal(actualNode.getName())){
        goalNode = actualNode;
        break;
      }

      for(A edge : actualNode.getAdjacenciesList()) {
        S targetState = prob.result(actualNode.getName(),edge);
        double targetEdgeWeight = prob.cost(actualNode.getName(),edge);
        if(!setOfStates.contains(targetState))
        {
          Node<S,A> targetNode = null;
          boolean exists = false;
          if(nodes_weights.get(targetState) != null) {
            targetNode = nodes_weights.get(targetState);
          } else {
            targetNode = new Node<>(targetState);
            nodes_weights.put(targetState,targetNode);
          }

          double newDistance = actualNode.getDistance() + targetEdgeWeight;
          if( newDistance < targetNode.getDistance() ) {
            priorityQueue.remove(targetNode);
            targetNode.setDistance(newDistance);
            targetNode.setPredecessor(actualNode);
            targetNode.setAction(edge);
            priorityQueue.add(targetNode);
          }
        }
      }
      setOfStates.add(actualNode.getName());
    }

    if (goalNode == null){
      System.out.println("can't reach destination");
      return null;
    }

    List<A> path = new ArrayList<>();
    for(Node<S,A> Node=goalNode;Node!=null;Node=Node.getPredecessor()) {
      if(Node.getAction()!=null){
        path.add(Node.getAction());
      }
    }
    Collections.reverse(path);
    Solution<S,A> solution = new Solution<S,A>(path,goalNode.getName(),goalNode.getDistance());
    return solution;
  }
}


class Node<S, A> implements Comparable<Node<S,A>> {
  private S name;//edge
  private List<A> adjacenciesList;
  private boolean visited;
  private Node<S,A> predecessor;
  private A action;
  private double distance = Double.MAX_VALUE;

  public Node(S name) {
    this.name = name;
    this.adjacenciesList = new ArrayList<>();
  }

  public S getName() {
    return name;
  }

  public void setName(S name) {
    this.name = name;
  }

  public List<A> getAdjacenciesList() {
    return adjacenciesList;
  }

  public void setAdjacenciesList(List<A> adjacenciesList) {
    this.adjacenciesList = adjacenciesList;
  }

  public A getAction() {
    return action;
  }

  public void setAction(A action) {
    this.action = action;
  }

  public boolean isVisited() {
    return visited;
  }

  public void setVisited(boolean visited) {
    this.visited = visited;
  }

  public Node<S,A> getPredecessor() {
    return predecessor;
  }

  public void setPredecessor(Node predecessor) {
    this.predecessor = predecessor;
  }

  public double getDistance() {
    return distance;
  }

  public void setDistance(double distance) {
    this.distance = distance;
  }

  @Override
  public String toString() {
    return "State"+name;
  }

  @Override
  public int compareTo(Node otherNode) {
    return Double.compare(this.distance, otherNode.getDistance());
  }

  @Override
  public boolean equals(Object o) {
    if (this == o) return true;
    if (o == null || getClass() != o.getClass()) return false;
    Node<?, ?> node = (Node<?, ?>) o;
    return visited == node.visited && Double.compare(node.distance, distance) == 0 && Objects.equals(name, node.name) && Objects.equals(adjacenciesList, node.adjacenciesList) && Objects.equals(predecessor, node.predecessor);
  }

  @Override
  public int hashCode() {
    return Objects.hash(name, adjacenciesList, visited, predecessor, distance);
  }
}