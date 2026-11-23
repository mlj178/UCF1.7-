public struct DamageTag
{
	public int tag { get; private set; }

	public bool isHitLower
	{
		get
		{
			return false;
		}
		set
		{
		}
	}

	public bool isBigshot
	{
		get
		{
			return false;
		}
		set
		{
		}
	}

	public bool isGhostBladeSecKill
	{
		get
		{
			return false;
		}
		set
		{
		}
	}

	public bool isMasterHeroSlash
	{
		get
		{
			return false;
		}
		set
		{
		}
	}

	public bool isArcane
	{
		get
		{
			return false;
		}
		set
		{
		}
	}

	public bool isCritical
	{
		get
		{
			return false;
		}
		set
		{
		}
	}

	public DamageTag(int tag)
	{
		this.tag = 0;
	}

	public void SetState(int bit, bool enable)
	{
	}

	public bool GetState(int bit)
	{
		return false;
	}
}
