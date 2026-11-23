public class WPN_MasterHero : WPN_Knife
{
	private WD_MasterHero realData2;

	private Skill_Common skill;

	public override void Init()
	{
	}

	private void WPN_MasterHero_KnifeAttackHit_Listener(int attackIndex, Entity victim)
	{
	}

	public override void Deploy(bool noSelectAnim = false)
	{
	}

	public override void UnDeploy(bool temporary = false)
	{
	}

	private bool MasterHeroSkill(Player player)
	{
		return false;
	}

	protected override int GetKnifeAttackSprIndex(int attackIndex)
	{
		return 0;
	}

	protected override string GetKnifeHitSoundName(int attackIndex)
	{
		return null;
	}

	protected override string GetKnifeHitEffectName(int attackIndex)
	{
		return null;
	}

	public override void BotControl(Bot bot)
	{
	}
}
