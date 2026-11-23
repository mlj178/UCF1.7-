public struct BotAbility
{
	public float zoomSpeed { get; private set; }

	public float shootAccuracy { get; private set; }

	public float recoilControl_X { get; private set; }

	public float recoilControlRange_X { get; private set; }

	public float randomRecoilControl_X => 0f;

	public float recoilControl_Y { get; private set; }

	public float recoilControlRange_Y { get; private set; }

	public float randomRecoilControl_Y => 0f;

	public void SetAbility(float ability)
	{
	}
}
