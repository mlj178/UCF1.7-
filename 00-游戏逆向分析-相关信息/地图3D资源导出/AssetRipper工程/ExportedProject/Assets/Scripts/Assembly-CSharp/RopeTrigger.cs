using UnityEngine;

public class RopeTrigger : MapTrigger
{
	[SerializeField]
	private Vector3 startPoint;

	[SerializeField]
	private Vector3 endPoint;

	public override void StartInteract(Player player)
	{
	}

	public override void Active(Player player)
	{
	}

	private void OnDrawGizmosSelected()
	{
	}
}
