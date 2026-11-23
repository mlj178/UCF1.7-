using System;
using System.Collections.Generic;
using Pathfinding;
using UnityEngine;

public class Bot_JumpLink : GraphModifier
{
	[Serializable]
	public struct Link
	{
		public Transform endTransform;

		[NonSerialized]
		public GraphNode endNode;

		public float needSpeed;

		public float accuracy;

		[NonSerialized]
		public Vector3 direction;

		public static Link empty;

		public void CaculateDirection(Transform startPoint)
		{
		}
	}

	public static Dictionary<GraphNode, Bot_JumpLink> linkDic;

	public Link[] links;

	public GraphNode startNode { get; private set; }

	public static bool GetLink(GraphNode graphNode, out Bot_JumpLink jumpLink)
	{
		jumpLink = null;
		return false;
	}

	public override void OnLatePostScan()
	{
	}

	public bool GetLinkEndByGraphNode(GraphNode node, out Link output)
	{
		output = default;
		return false;
	}

	private void OnDrawGizmosSelected()
	{
	}
}
