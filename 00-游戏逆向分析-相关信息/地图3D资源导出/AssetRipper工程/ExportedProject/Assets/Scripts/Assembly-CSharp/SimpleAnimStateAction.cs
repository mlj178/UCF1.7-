using UnityEngine;

public class SimpleAnimStateAction : StateMachineBehaviour
{
	[SerializeField]
	private string Enter_ActionName;

	[SerializeField]
	private string Enter_Data;

	[SerializeField]
	private string Exit_ActionName;

	[SerializeField]
	private string Exit_Data;

	public override void OnStateEnter(Animator animator, AnimatorStateInfo stateInfo, int layerIndex)
	{
	}

	public override void OnStateExit(Animator animator, AnimatorStateInfo stateInfo, int layerIndex)
	{
	}
}
