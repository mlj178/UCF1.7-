using UnityEngine;

[CreateAssetMenu]
public class WD_GhostBlade : WeaponData_Knife
{
	public string btlModeWpnName;

	public CharWpnAnimData btlModeCharAnimData;

	public GameObject skillBtn;

	public override string GetWeaponName(int index)
	{
		return null;
	}
}
