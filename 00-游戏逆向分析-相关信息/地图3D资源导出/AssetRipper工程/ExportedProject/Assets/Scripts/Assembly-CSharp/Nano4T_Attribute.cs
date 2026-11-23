using System;
using UnityEngine;

[Serializable]
public class Nano4T_Attribute
{
	public static Nano4T_Attribute None;

	public string attributeName;

	public int id;

	public Sprite image;

	public string description;

	public const int Gene = 0;

	public const int Terminator = 1;

	public const int Upgrade = 2;

	public const int Strong = 3;

	public const int Armor = 4;

	public const int Nail = 5;

	public const int InfectExp = 6;

	public const int Hot = 7;

	public const int EvilBox = 8;

	public const int Grave = 9;

	public const int Savior = 10;

	public const int KillNano = 11;

	public const int Grenade = 12;

	public const int Supply = 13;

	public const int Ammo = 14;

	public const int Reload = 15;

	public const int Shield = 16;

	public const int SPAgent = 17;

	public const int HeroBox = 18;

	public const int Critical = 19;

	public string GetDescription(bool isNano, bool withName)
	{
		return null;
	}

	public bool IsMax10()
	{
		return false;
	}

	public bool IsSkillAttribute()
	{
		return false;
	}
}
