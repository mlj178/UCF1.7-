using CodeStage.AntiCheat.ObscuredTypes;

public class WeaponBag
{
	public ObscuredBool disabled;

	public ObscuredBool tooFarFromSpawnPos;

	public const float allowDistance = 20f;

	public bool[] available;

	public int[][] weaponID;

	public int currentBagID;

	public void LoadData(ClientData clientData)
	{
	}

	public int GetRandomBagID()
	{
		return 0;
	}

	public bool EquipAnyVVIPWeapon()
	{
		return false;
	}
}
