public class SpeedBuff : Buff
{
	public float moveSpeedPenalty;

	public SpeedBuff(string name, float duration, Entity owner, float penalty)
		: base(null, 0f, null)
	{
	}

	private void SpeedPenaltyBuffUpdate(ref float speedUp, ref float speedDown)
	{
	}

	protected override void OnLifeEnd()
	{
	}
}
