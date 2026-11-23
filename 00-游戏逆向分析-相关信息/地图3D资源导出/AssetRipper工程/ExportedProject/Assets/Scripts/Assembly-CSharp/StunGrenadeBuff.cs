public class StunGrenadeBuff : SpeedBuff
{
	public static string BuffName;

	public StunGrenadeBuff(Entity owner)
		: base(null, 0f, null, 0f)
	{
	}

	private void BuffUpdater(ref bool value)
	{
	}

	protected override void OnLifeEnd()
	{
	}
}
