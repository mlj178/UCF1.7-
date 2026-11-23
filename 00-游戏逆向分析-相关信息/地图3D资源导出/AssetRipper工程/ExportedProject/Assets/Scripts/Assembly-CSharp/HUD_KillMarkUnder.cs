using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

public class HUD_KillMarkUnder : Singleton<HUD_KillMarkUnder>
{
	public enum Type
	{
		Common = 0,
		Melee = 1,
		Headshot = 2,
		Headshot_Gold = 3
	}

	public GameObject prefab;

	public Sprite[] sprites;

	private List<Image> markList;

	private static int currentCount;

	private static int tenCounter;

	protected override void Awake()
	{
	}

	public static void AddMark(Type type)
	{
	}

	private static void Shrink()
	{
	}
}
