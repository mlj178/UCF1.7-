public class WPN_EvilTerminator : WPN_Knife
{
	private WD_EvilTerminator realData2;

	private Skill_Common skill;

	private float startPowerTime;

	private float powerProgress;

	private const float PowerTime = 6f;

	private const float MaxHoldTime = 9f;

	private RecyclableSound curPowerSnd;

	private int sndState;

	private EffectObj FX_3rd;

	private EffectObj FX_PV;

	private bool isPowering => false;

	protected override void Update()
	{
	}

	public override void Init()
	{
	}

	public override void Deploy(bool noSelectAnim = false)
	{
	}

	public override void UnDeploy(bool temporary = false)
	{
	}

	private bool EvilTerminatorSkill(Player player)
	{
		return false;
	}

	protected override void OnAnimationEnd(string animName, string animTag)
	{
	}

	private void ThrowFireBall()
	{
	}

	private void FireBallSetting(WPN_Missile missile)
	{
	}

	private void EffectSndEvent()
	{
	}

	private void ClearPowerSound()
	{
	}

	private void ClearPowerEffect()
	{
	}

	private void CreatePowerEffect()
	{
	}

	private void UpdateEffectSize(float progress)
	{
	}

	public override void BotControl(Bot bot)
	{
	}
}
