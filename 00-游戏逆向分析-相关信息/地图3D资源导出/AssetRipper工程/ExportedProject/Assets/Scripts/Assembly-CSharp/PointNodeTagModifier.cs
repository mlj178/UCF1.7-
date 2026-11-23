using Pathfinding;
using UnityEngine;

public class PointNodeTagModifier : GraphModifier
{
	[SerializeField]
	private Vector3[] points;

	[SerializeField]
	private uint pathTag;

	public override void OnLatePostScan()
	{
	}

	private void OnDrawGizmosSelected()
	{
	}
}
