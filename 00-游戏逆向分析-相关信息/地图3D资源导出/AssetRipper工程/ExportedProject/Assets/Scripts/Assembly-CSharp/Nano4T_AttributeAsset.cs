using System;
using BotAction.Skill;
using UnityEngine;

[CreateAssetMenu]
public class Nano4T_AttributeAsset : ScriptableObject
{
	[Serializable]
	public class Group
	{
		public RandomItem nano;

		public RandomItem human;
	}

	[SerializeField]
	private Group normalRound;

	[SerializeField]
	private Group battleRound;

	[SerializeField]
	private Nano4T_Attribute[] attributes;

	[SerializeField]
	private GameObject SkillBtn_GoldShield;

	[SerializeField]
	private GameObject SFX_GoldShield;

	[SerializeField]
	private GameObject FX_GoldShield;

	[SerializeField]
	private GameObject SkillBtn_SPAgent;

	[SerializeField]
	private GameObject FX_SPAgent;

	public GameObject TombStone;

	public void Init()
	{
	}

	public Nano4T_Attribute GetAttribute(bool isNano)
	{
		return null;
	}

	private Nano4T_Attribute GetAttribute(int id)
	{
		return null;
	}

	public void SetSkill_GoldShield(Player player)
	{
	}

	private bool Skill_GoldShield(Player player)
	{
		return false;
	}

	private BotSkillBase SkillAI_GoldShield(Bot bot)
	{
		return null;
	}

	public void SetSkill_SPAgent(Player player)
	{
	}

	private bool Skill_SPAgent(Player player)
	{
		return false;
	}

	private BotSkillBase SkillAI_SPAgent(Bot bot)
	{
		return null;
	}
}
