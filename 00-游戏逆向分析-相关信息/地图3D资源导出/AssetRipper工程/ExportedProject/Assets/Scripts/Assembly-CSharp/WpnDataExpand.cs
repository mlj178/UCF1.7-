public static class WpnDataExpand
{
	public static bool IsMainWeapon(this WeaponClass wpnClass)
	{
		return false;
	}

	public static bool IsThrowWeapon(this WeaponClass wpnClass)
	{
		return false;
	}

	public static int GetSlotID(this WeaponClass wpnClass)
	{
		return 0;
	}
}
