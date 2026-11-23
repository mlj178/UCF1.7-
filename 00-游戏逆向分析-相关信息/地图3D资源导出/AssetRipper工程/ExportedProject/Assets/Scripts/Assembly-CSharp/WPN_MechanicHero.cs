using BotAction.Skill;

public class WPN_MechanicHero : WPN_Knife
{
	private WD_MechanicHero realData2;

	private Skill_Common skill_Arcane;

	private Skill_SentryGun skill_SentryGun;

	public override void Init()
	{
	}

	protected override void SetValidOwner()
	{
	}

	protected override void RemoveFromOldOwner()
	{
	}

	private bool SkillArcane(Player player)
	{
		return false;
	}

	private bool SkillSentryGun(Player player)
	{
		return false;
	}

	private BotSkillBase SkillAI_Arcane(Bot bot)
	{
		return null;
	}

	private BotSkillBase SkillAI_SentryGun(Bot bot)
	{
		return null;
	}
}
