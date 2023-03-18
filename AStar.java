import java.util.*;
import search.HeuristicProblem;
import search.Solution;

public class AStar<S, A> {
  public static <S, A> Solution<S, A> search(HeuristicProblem<S, A> prob) {
    S initState = prob.initialState();
    Set<S> setOfStates = new HashSet<S>();
    Node<S,A> sourceNode = new Node<S,A>(initState);
    sourceNode.setDistance(0);
    sourceNode.setVisited(false);
    sourceNode.setPredecessor(null);
    sourceNode.setAction(null);
    sourceNode.estimatedCostToGoal = prob.estimate(sourceNode.getName());
    sourceNode.f = sourceNode.distance + sourceNode.estimatedCostToGoal;

    Node<S,A> goalNode = null;

    PriorityQueue<Node<S,A>> priorityQueue = new PriorityQueue<Node<S,A>>(new Comparator<Node>() {
      @Override
      public int compare(Node node0, Node node1) {
        return Double.compare(node0.f, node1.f);
      }
    });

    priorityQueue.add(sourceNode);

    while (!priorityQueue.isEmpty() ) {
      Node<S, A> actualNode = priorityQueue.poll();
      if (actualNode.isVisited()){
        continue;
      }
      if(setOfStates.contains(actualNode.getName())){
        continue;
      }
      actualNode.setVisited(true);
      setOfStates.add(actualNode.getName());

      if (prob.isGoal(actualNode.getName())) {
        goalNode = actualNode;
        break;
      }

      for (A edge : prob.actions(actualNode.getName())) {
        S targetState = prob.result(actualNode.getName(), edge);
        if (!setOfStates.contains(targetState)){
          Node<S,A> targetNode = new Node<>(prob.result(actualNode.getName(), edge));
          targetNode.setPredecessor(actualNode);
          targetNode.setAction(edge);
          targetNode.distance = actualNode.distance + prob.cost(actualNode.getName(), edge);
          targetNode.estimatedCostToGoal = prob.estimate(targetNode.getName());
          targetNode.f = targetNode.distance + targetNode.estimatedCostToGoal;
          priorityQueue.add(targetNode);
        }
      }
    }

    if (goalNode == null) {
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

class Node<S, A> {
  private S name; //edge
  private List<A> adjacenciesList;
  private boolean visited;
  private Node<S,A> predecessor;
  private A action;
  public double distance;
  public double estimatedCostToGoal;
  public double f;

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

  public void setPredecessor(Node<S,A> predecessor) {
    this.predecessor = predecessor;
  }

  public double getDistance() {
    return distance;
  }

  public void setDistance(double distance) {
    this.distance = distance;
  }
}