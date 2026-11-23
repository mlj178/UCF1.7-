public static class NanoRoleExpand
{
	public static string GetName(this NanoRole role)
	{
		return null;
	}

	public static bool IsSoldierOrSavior(this NanoRole role)
	{
		return false;
	}

	public static bool LikeGuard(this NanoRole role)
	{
		return false;
	}

	public static bool IsHuman(this NanoRole role)
	{
		return false;
	}

	public static bool IsHero(this NanoRole role)
	{
		return false;
	}

	public static bool IsNormalHero(this NanoRole role)
	{
		return false;
	}

	public static bool IsMasterHero(this NanoRole role)
	{
		return false;
	}

	public static bool IsNanoGhost(this NanoRole role)
	{
		return false;
	}

	public static bool IsNormalNanoGhost(this NanoRole role)
	{
		return false;
	}

	public static bool IsTerminator(this NanoRole role)
	{
		return false;
	}

	public static bool IsNormalTerminator(this NanoRole role)
	{
		return false;
	}

	public static bool IsMasterTerminator(this NanoRole role)
	{
		return false;
	}

	public static Team GetTeam(this NanoRole role)
	{
		return Team.BlackList;
	}

	public static bool ShouldRemoveAllWpn(this NanoRole role)
	{
		return false;
	}

	public static bool CanUseGun(this NanoRole role)
	{
		return false;
	}
}
