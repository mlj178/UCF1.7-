using System.Collections.Generic;
using UnityEngine;

public class Bot_NanoGuardArea : MonoBehaviour
{
	public static List<Bot_NanoGuardArea> SpareAreaList;

	public Vector3[] entrancePos;

	private List<Bot_NanoGuardPos> posList;

	[SerializeField]
	private Bot_NanoGuardArea[] neighborAreas;

	[SerializeField]
	private Bot_NanoGuardArea[] escapeAreas;

	[SerializeField]
	private Vector3[] escapePos;

	public bool isFull => false;

	private void Awake()
	{
	}

	private void OnTriggerEnter(Collider other)
	{
	}

	private void OnTriggerExit(Collider other)
	{
	}

	public Bot_NanoGuardPos GetPos()
	{
		return null;
	}

	public void RecyclePos(Bot_NanoGuardPos pos)
	{
	}

	public static Bot_NanoGuardArea GetRandomArea()
	{
		return null;
	}

	public bool GetRandomEscapePos(out Vector3 pos)
	{
		pos = default;
		return false;
	}

	public static Bot_NanoGuardArea GetRandomAreaExclude(Bot_NanoGuardArea exclude)
	{
		return null;
	}

	private void OnDrawGizmosSelected()
	{
	}

	public Bot_NanoGuardPos GetSaferPos(int safety)
	{
		return null;
	}

	public Bot_NanoGuardArea GetEscapeArea()
	{
		return null;
	}

	public Bot_NanoGuardArea GetNeighborArea()
	{
		return null;
	}
}
