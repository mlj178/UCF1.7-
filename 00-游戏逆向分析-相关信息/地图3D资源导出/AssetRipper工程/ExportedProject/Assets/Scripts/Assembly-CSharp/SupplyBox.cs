using System.Collections.Generic;
using UnityEngine;

public class SupplyBox : RecyclableObject
{
	public enum Type
	{
		Yellow = 0,
		Red = 1,
		Blue = 2
	}

	[SerializeField]
	private Type type;

	private int occupiedPosID;

	public static List<SupplyBox> BoxList_Yellow;

	public static List<SupplyBox> BoxList_Red;

	public static List<SupplyBox> BoxList_Blue;

	private void OnTriggerStay(Collider other)
	{
	}

	public bool CanPickUp(Player player)
	{
		return false;
	}

	public static bool CanPickUpRedBox(Player player)
	{
		return false;
	}

	public void SetPos(int index, SpawnPoint point)
	{
	}

	public override void Recycle(bool roundRecycle)
	{
	}

	protected override void Work()
	{
	}

	private static List<SupplyBox> GetBoxList(Type boxType)
	{
		return null;
	}

	public static SupplyBox GetRandomBox(Type boxType)
	{
		return null;
	}

	public static SupplyBox GetNearestBox(Type boxType, Vector3 pos)
	{
		return null;
	}

	public static void ClearBoxList()
	{
	}

	public Type GetBoxType()
	{
		return Type.Yellow;
	}
}
