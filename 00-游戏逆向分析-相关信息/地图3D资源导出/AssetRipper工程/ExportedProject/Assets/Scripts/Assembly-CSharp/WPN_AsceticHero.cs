using BotAction.Skill;

public class WPN_AsceticHero : WPN_Knife
{
	private WD_AsceticHero realData2;

	private Skill_Common skill;

	private bool comboFinishTag;

	private int shieldHealth;

	private const int DefenseDamage = 5000;

	private RecyclableObject shieldSound;

	public override void Init()
	{
	}

	private void PostCalDamage(ref DamageEventData data)
	{
	}

	protected override void Update()
	{
	}

	protected override void OnAnimationEnter(string animName, string animTag)
	{
	}

	protected override void OnKnifeAttackAnimEnd(string animName)
	{
	}

	private void FinishCombo()
	{
	}

	public override void Deploy(bool noSelectAnim = false)
	{
	}

	public override void UnDeploy(bool temporary = false)
	{
	}

	private bool AsceticHeroSkill(Player player)
	{
		return false;
	}

	private void Shield2()
	{
	}

	private void ShieldBlast()
	{
	}

	private BotSkillBase SkillAI_AsceticHero(Bot bot)
	{
		return null;
	}
}
