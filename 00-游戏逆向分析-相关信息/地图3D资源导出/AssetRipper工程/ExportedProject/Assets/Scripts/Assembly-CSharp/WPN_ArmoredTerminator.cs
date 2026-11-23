using System;
using UnityEngine;

public class WPN_ArmoredTerminator : WPN_Knife
{
	private Skill_Common skill;

	[SerializeField]
	private GameObject skillBtn;

	[SerializeField]
	private GameObject effect;

	[SerializeField]
	private GameObject fearSign;

	private static readonly float threatenRange;

	protected override void SetValidOwner()
	{
	}

	protected override void RemoveFromOldOwner()
	{
	}

	public override void Deploy(bool noSelectAnim = false)
	{
	}

	private bool Cry(Player player)
	{
		return false;
	}

	protected override void OnAnimationEnd(string animName, string animTag)
	{
	}

	private void CryTrigger()
	{
	}

	private void Overlap(Action<Player> func)
	{
	}

	private void AddSlowDebuf(Player target)
	{
	}

	public static void Threaten(Player target)
	{
	}
}
