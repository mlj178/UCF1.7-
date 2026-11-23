using UnityEngine;

public class WD_SkillKnife : WeaponData_Knife, ISkillBtnGetter
{
	public GameObject skillBtn;

	public GameObject GetSkillBtn(int index)
	{
		return null;
	}

	public override Sprite GetKillMsgIcon(int index)
	{
		return null;
	}
}
