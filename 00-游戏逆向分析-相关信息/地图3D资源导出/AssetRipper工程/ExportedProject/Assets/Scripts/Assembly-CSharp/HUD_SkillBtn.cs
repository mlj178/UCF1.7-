using System;
using UnityEngine;
using UnityEngine.UI;

public class HUD_SkillBtn : RecyclableObject
{
	[NonSerialized]
	public int curPos;

	[SerializeField]
	private Image image;

	[SerializeField]
	private Sprite[] btnSprs;

	public Skill bindSkill;

	private void Update()
	{
	}

	public void SetPos(int pos)
	{
	}

	public override void Recycle(bool roundRecycle)
	{
	}
}
