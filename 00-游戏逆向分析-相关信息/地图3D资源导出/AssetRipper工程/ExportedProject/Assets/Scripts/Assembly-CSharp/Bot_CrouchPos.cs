using System.Collections.Generic;
using UnityEngine;

public class Bot_CrouchPos : Bot_GuardPos
{
	[SerializeField]
	private bool crouchDisabled;

	[SerializeField]
	private bool always;

	private static List<Bot_CrouchPos> SpareList_BL;

	private static List<Bot_CrouchPos> SpareList_GR;

	public bool isAlways => false;

	private void Awake()
	{
	}

	private void AddToSpareList()
	{
	}

	private void RemoveFromSpareList()
	{
	}

	protected override void OnSetNullOwner()
	{
	}

	protected override void OnSetValidOwner()
	{
	}

	public static void Clear()
	{
	}

	public static Bot_CrouchPos GetRandomPos(Team playerTeam)
	{
		return null;
	}
}
